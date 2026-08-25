# S2 — EVIDENCE COLLECTION STAGE smoke test log

Session: session_2026-08-25-pipeline-smoke-test-mobility
Agent: S2 (evidence-collection stage)
Repo HEAD: ce33ef60b9d5247f3c2702ada545146c23bee8c5
data/guidebook.db sha256 at start: 30a106692ab4110fe4e2082018eb256a325b2884d5740d3f62445b52c07dceaf (matches expected 30a10669...)
data/guidebook.db sha256 at end:   30a106692ab4110fe4e2082018eb256a325b2884d5740d3f62445b52c07dceaf (UNCHANGED — verified)
Scratch DB: $SMOKE/s2-evidence.db (copied from canonical at session start, sha256-verified identical before first write)
Retrieval log for this run: `$SMOKE/retrieval-log-s2/` (kept OUT of the tracked `retrieval-log/` tree per PROTOCOL rule 3 — nothing tracked was written)
Start time (UTC): 2026-08-25 18:20

Real subject used throughout: Sanford JA, Story MF, Jones ML (1997), "An Analysis of the
Effects of Ramp Slope on People with Mobility Impairments", *Assistive Technology* 9(1):22-33,
DOI `10.1080/10400435.1997.10132293` — directly on-topic for item E-03 (ramp gradient) /
slug `stair-ramp-threshold-biomechanics-accessibility`. Found via a real Crossref bibliographic
search, retrieved via `retrieval_log.fetch()` (R10 leg 1), DOI-resolution cross-checked via
`doi.org` (R10 leg 2, 302 → tandfonline.com abstract page; direct fetch of the publisher page
itself returned HTTP 403, ordinary bot-blocking, not a metadata problem). Admitted for real as
`REF-00971` on the scratch DB. This is the only source actually "admitted" in this run; every
other write is either a refusal probe or is clearly marked `[SMOKE-TEST PLACEHOLDER]` and never
represented as real evidence.

---

## PART 1 — Admission path end to end (task 1)

### 1. Crossref bibliographic search (R10 leg 0 — finding the source)
INVOKED   : `curl https://api.crossref.org/works?query.bibliographic=Sanford+Story+Jones+ramp+slope+mobility+impairments&rows=5`
STAGE     : evidence-collection (research boundary — this is the last hop before admission)
EXIT      : 0   RUNTIME: ~1s
READS     : network (api.crossref.org)
WRITES    : NONE (raw curl, not yet through the logged fetch path)
EXAMINED  : 5 candidate records returned
OUTPUT    : top hit `10.1080/10400435.1997.10132293` "An Analysis of the Effects of Ramp Slope on People with Mobility Impairments" — Sanford/Story/Jones
FINDING   : PASS
LOCATION  : n/a
NOTE      : A real, on-topic, retrievable mobility source exists and is trivially findable — the corpus problem for item E-03 is not "no literature exists."

### 2. Retrieval, logged (R10 leg 1 — Crossref canonical record)
INVOKED   : `GUIDEBOOK_RETRIEVAL_LOG=$SMOKE/retrieval-log-s2 python3 -c "...retrieval_log.fetch('https://api.crossref.org/works/10.1080/10400435.1997.10132293', session=SESSION, purpose='R10 leg1...')"`
STAGE     : evidence-collection
EXIT      : 0   RUNTIME: ~1s
READS     : `scripts/research/retrieval_log.py:118-143` (`fetch`)
WRITES    : `$SMOKE/retrieval-log-s2/<session>/0bb880bf0ac7b2c5.json` (5453 bytes) + `manifest.jsonl` (url, purpose, sha256, bytes, exit, artefact — `retrieval_log.py:132-137`)
EXAMINED  : 1 payload
OUTPUT    : sha256 `0bb880bf0ac7b2c533363b6eaa43bd4fd42d1d87f08b0b9a1707d9fc503462da` — **byte-identical** to an independent manual `curl` of the same URL done seconds earlier, confirming `fetch()` persists exactly what it acted on
FINDING   : PASS
LOCATION  : `scripts/research/retrieval_log.py:118-143`
NOTE      : Artefact discipline works exactly as designed (see PART 9 below for the full offline-diff proof).

### 3. R10 leg 2 — DOI resolution / publisher cross-check
INVOKED   : `curl -D - https://doi.org/10.1080/10400435.1997.10132293` (1 probe, per PROTOCOL rule 4)
STAGE     : evidence-collection
EXIT      : 0   RUNTIME: ~1s
READS     : network (doi.org)
WRITES    : NONE
EXAMINED  : 1
OUTPUT    : `HTTP/2 302` → `location: http://www.tandfonline.com/doi/abs/10.1080/10400435.1997.10132293`
FINDING   : PASS
LOCATION  : n/a
NOTE      : DOI resolves to the correct publisher record. A direct fetch of the tandfonline abstract page itself returned HTTP 403 (ordinary bot-blocking on a paywalled article page) — logged as the expected shape of a blocked leg, not mined further per rule 4.

### 4. `db.py add-source` — dry-run + `--slug`/`--local-ref-id` (found a real bug)
INVOKED   : `python3 scripts/db.py add-source --ref-id REF-00971 ... --slug stair-ramp-threshold-biomechanics-accessibility --local-ref-id SRT-01 --session $SESSION --dry-run`
STAGE     : evidence-collection
EXIT      : 1   RUNTIME: <1s
READS     : `scripts/db.py:1508-1553` (`add-source` dispatch), `scripts/dbcore.py:82-120` (`connect`)
WRITES    : NONE (crashed before commit)
EXAMINED  : n/a — crashed
OUTPUT    : `sqlite3.IntegrityError: FOREIGN KEY constraint failed` at `scripts/db.py:2032` (inside `insert_source_slug_link`)
FINDING   : FAIL (real defect, not a doctrine refusal)
LOCATION  : `scripts/db.py:1548-1552` (two separate `insert_evidence_source` / `insert_source_slug_link` calls, each opening its **own** `with dbcore.connect(dry_run)` block) × `scripts/dbcore.py:108-118` (`dry_run` → `conn.rollback()`)
NOTE      : **`add-source --dry-run` combined with `--slug`/`--local-ref-id` cannot be exercised as a dry run at all.** `insert_evidence_source`'s transaction rolls back (dbcore.py:113-115) before `insert_source_slug_link` opens its own connection and tries to INSERT a `source_slug_links` row FK-referencing a `ref_id` that, in dry-run mode, was never actually committed — so the second half of the very call the CLI advertises as one operation throws an unhandled `IntegrityError` instead of demonstrating anything. A session using `--dry-run` to preview a slug-linked admission (the documented use case) gets a stack trace, not a preview. Real (non-dry-run) admission is unaffected — confirmed next.

### 5. `db.py add-source` — the real admission
INVOKED   :
```
python3 scripts/db.py add-source --ref-id REF-00971 \
  --author "Sanford|Jon A." --author "Story|Molly Follette" --author "Jones|Michael L." \
  --year 1997 --title "An Analysis of the Effects of Ramp Slope on People with Mobility Impairments" \
  --tier 1 --doi 10.1080/10400435.1997.10132293 --evidence-type empirical --pages "22-33" \
  --url "https://doi.org/10.1080/10400435.1997.10132293" --url-accessed "2026-08-25" \
  --doi-resolution-outcome RESOLVED --metadata-quality COMPLETE \
  --verification-status VERIFIED --verification-method tool --verified-by-tool crossref \
  --slug stair-ramp-threshold-biomechanics-accessibility --local-ref-id SRT-01 --session $SESSION
```
STAGE     : evidence-collection
EXIT      : 0   RUNTIME: <1s
READS     : `scripts/db.py:1508-1553`, `insert_evidence_source` (`scripts/db.py:1863-2025`), `insert_source_slug_link` (`scripts/db.py:2028-2038`)
WRITES    : `evidence_sources` @ ref_id=REF-00971 (all fields below) · `evidence_source_authors` @ ref_id=REF-00971, positions 1-3 (Sanford/Story/Jones) · `source_slug_links` @ (REF-00971, stair-ramp-threshold-biomechanics-accessibility)
EXAMINED  : 1 admission
OUTPUT    : `{"ref_id": "REF-00971", "linked_slug": "stair-ramp-threshold-biomechanics-accessibility", "dry_run": false}`
FINDING   : PASS (mechanically) — **but see NOTE and PART 4/PART 6 for two downstream defects this exact admission exposed**
LOCATION  : n/a
NOTE      : The admission itself succeeds and does exactly what CLAUDE.md §4 documents: `url`, `pages`, `doi_resolution_outcome` all landed (the Act-2 closure is real — confirmed by inspection too, see refusal #9 below). **But this single, honestly-sourced, correctly-verified admission goes on to fail two separate downstream integrity checks** (blocking `test_db_integrity.py` I1 — PART 4 — and `adjudication_integrity.py`'s tier-derivation check — PART 6) purely because of gaps in what the CLI lets you set, not because of anything wrong with the sourcing. This is the headline finding of this run; see the SUMMARY.

### 6. Offline author/biblio fidelity check on the new admission
INVOKED   : `GUIDEBOOK_RETRIEVAL_LOG=$SMOKE/retrieval-log-s2 GUIDEBOOK_DB_PATH=$SMOKE/s2-evidence.db python3 scripts/research/retrieval_log.py --verify-authors --session $SESSION`
STAGE     : evidence-collection
EXIT      : 0   RUNTIME: <1s, no network
READS     : `$SMOKE/retrieval-log-s2/<session>/manifest.jsonl` + artefact, `evidence_sources`, `evidence_source_authors` (scratch DB, read-only)
WRITES    : NONE
EXAMINED  : 1 (the only DOI-bearing source with a logged payload under this session)
OUTPUT    : `CLEAN — stored authors and asserted bibliographic fields match the retrieved payloads, byte-for-byte source.` plus a **reported, not failed** gap: `volume is NULL; payload has '9'` / `issue is NULL; payload has '1'`
FINDING   : PASS (authors) / gap noted (volume, issue)
LOCATION  : `scripts/research/retrieval_log.py:240-320`
NOTE      : Author fidelity for my own admission is perfect — the mechanism that would have caught the 2026-08-19 fabrication works. The volume/issue gap is not a mistake on my part: **`add-source` has no `--volume` or `--issue` flag at all** (confirmed by grep — see PART 5 finding). The row is stamped `metadata_quality='COMPLETE'` while genuinely missing two fields the payload supplied, which is exactly the failure class this verifier's docstring describes (REF-00968's `pages`/`article-number` mis-file, 2026-08-22) — reproduced fresh, mechanically, with real payload evidence, not asserted from memory.

---

## PART 2 — Every refusal `add-source` makes (task 2)

All run with `GUIDEBOOK_DB_PATH=$SMOKE/s2-evidence.db`, `--session $SESSION`.

### 7. Missing `--tier`
EXIT: 2. `db.py add-source: error: the following arguments are required: --tier` — argparse-level, before any DB touch. FINDING: PASS. LOCATION: `scripts/db.py:1081` (`required=True`).

### 8. Invalid `--ref-id` shape (local label given as global id)
EXIT: 1. `ValueError: --ref-id 'SRT-02' is not a global reference id. 'SRT-02' looks like a per-slug LOCAL label...` FINDING: PASS — names the exact mistake and the fix. LOCATION: `scripts/db.py:1933-1945`.

### 9. Duplicate `--ref-id` (REF-00971 again)
EXIT: 1. `ValueError: REF-00971 already exists. R9: cross-file the existing ref_id rather than duplicating.` FINDING: PASS — not `INSERT OR IGNORE`, does not silently no-op (explicitly designed against that, per the comment at `scripts/db.py:1980-1984`). LOCATION: `scripts/db.py:1985-1991`.

### 10. Duplicate DOI **within `evidence_sources`** (new ref-id, REF-00971's DOI)
EXIT: 1. `ValueError: DOI 10.1080/10400435.1997.10132293 is already filed as REF-00971 (R9: pre-check the DOI, cross-file rather than duplicate).` FINDING: PASS. LOCATION: `scripts/db.py:1992-2000`.

### 11. Duplicate DOI **held only in `source_locators`** — **OD-5, proven live** (task 3)
INVOKED: `add-source --ref-id REF-00974 --doi 10.1192/bjp.bp.112.118422 ...` where that exact DOI is already `source_locators.ref_id='REF-00099'` (status `REFERENCE-ONLY`), and is **absent** from `evidence_sources`.
EXIT      : 0 (SUCCEEDED — no refusal)
OUTPUT    : `{"ref_id": "REF-00974", "linked_slug": null, "dry_run": false}`
FINDING   : **FAIL — OD-5 confirmed live**, by direct reproduction, not by re-reading the CLAUDE.md claim.
LOCATION  : `scripts/db.py:1992-2000` (`insert_evidence_source`'s dupe check queries `evidence_sources` only) — **contrast** `scripts/db.py:2513-2521` (`insert_locator`'s dupe check queries **both** `source_locators` and `evidence_sources`, case-folded via `dbcore.norm_doi`). Proven from the other direction too: `add-locator --doi 10.1080/10400435.1997.10132293` (REF-00971's DOI, held only in `evidence_sources`) **was correctly refused** — `ValueError: DOI ... is already held as REF-00971 in evidence_sources. R9: cross-file the existing ref_id...` (case 21 below).
NOTE      : This is the exact defect CLAUDE.md §4 flags as "a known live defect (OD-5)" and it is real: **`add-locator` was fixed to check both ref-id homes; `add-source` — the writer that actually creates a citable, synthesis-facing identity — was not.** A real mobility batch drawing from the 875-row `source_locators` clue store (the PROTOCOL's stated driver) can silently mint a second global identity for a lead that's already sitting there, with zero warning, every time the lead has a DOI. Two of the leads I sampled from `source_locators` for ramp/threshold/wheelchair keywords carry DOIs that look mismatched to their titles (`REF-00099` "NBR 9050:2020 §6.2 Rampas" ↔ DOI `10.1192/bjp.bp.112.118422`, a British Journal of Psychiatry DOI; `REF-00223` similarly) — pre-existing corpus noise that this exact gap would let a batch duplicate under a fresh identity without ever being told the lead already existed.

### 12. `VERIFIED` without `--verification-method`
EXIT: 1. `ValueError: VERIFIED requires --verification-method ... D-0157: a standing without its method is not a standing.` FINDING: PASS. LOCATION: `scripts/db.py:1961-1968`.

### 13. `--verification-method tool` without `--verified-by-tool`
EXIT: 1. `ValueError: verification_method='tool' requires --verified-by-tool ... (invariant I4b).` FINDING: PASS. LOCATION: `scripts/db.py:1969-1972`.

### 14. Invalid `--verification-status` value
EXIT: 2. `error: argument --verification-status: invalid choice: 'MAYBE' (choose from 'VERIFIED', 'UNVERIFIED')` — argparse `choices=`. FINDING: PASS. LOCATION: `scripts/db.py:1108-1110`.

### 15. No `--author`/`--authors`
EXIT: 2. `error: add-source needs --author (repeatable, preferred) or --authors`. FINDING: PASS. LOCATION: `scripts/db.py:1508-1510`.

### 16. Both `--author` and `--authors`
EXIT: 2. `error: give --author or --authors, not both: two spellings of the author list is the copy this migration removes`. FINDING: PASS (rule 5 enforced at the flag level). LOCATION: `scripts/db.py:1511-1513`.

### 17. `tier=99` — **no refusal at write time**
EXIT: 0 (SUCCEEDED). `{"ref_id": "REF-00972", ...}`, row lands with `tier=99`.
FINDING   : FAIL at write time / **PASS two stages later**. `evidence_sources.tier` has no CHECK constraint and `db.py` never calls `dbcore.check_vocab`/`check_declared` on it (confirmed: `grep check_vocab scripts/db.py` shows no call for `tier`). It **is** caught by `RANGE_GUARDS` in `scripts/emit_data_migration.py:96-97` at migration-emit time (task 6 below) and again by blocking `test_db_integrity.py` B11 (PART 4).
LOCATION  : write-time gap at `scripts/db.py` (no enforcement anywhere in `insert_evidence_source`); caught downstream at `scripts/emit_data_migration.py:96-97` and `scripts/tests/test_db_integrity.py` B10/B11.
NOTE      : The safety net is real but two stages removed from the point of writing — a session that writes and never runs `emit_data_migration.py`/`test_db_integrity.py` before shipping a hand-off would never see this.

### 18. `--doi-resolution-outcome MAYBE` — **no refusal anywhere in the write path's front two stages**
EXIT: 0 (SUCCEEDED). `{"ref_id": "REF-00973", ...}`.
FINDING   : **FAIL** — a genuinely novel, reproducible gap, not a restatement of an existing note.
LOCATION  : `scripts/db.py:1076-1078` (`--doi-resolution-outcome` has no `choices=`) → `scripts/emit_data_migration.py:66-73,101-133` (`ENUM_GUARDS`/`check_enum_guards`) → verified directly:
```
python3 -c "import emit_data_migration as edm; print(edm.check_enum_guards(open('batch.sql').read()))"
# => []   (no violation reported for doi_resolution_outcome='MAYBE')
```
NOTE      : `ENUM_GUARDS`' own docstring says positional `INSERT` statements are covered by scanning for a **hardcoded "suspicious" shortlist** (`NOT-APPLICABLE, N/A, NA, NONE, UNKNOWN, PENDING, NOT-CHECKED, UNRESOLVED`, `scripts/emit_data_migration.py:121-122`) — `'MAYBE'` isn't on it, and the batch SQL `emit_batch_sql.py` generates is always a positional `INSERT`, never an `UPDATE col='X'` (which is the only form the check's *full* enumeration check (Form 1) covers). **So a plausible-but-wrong value that isn't on the nine-word suspicious list sails through both `db.py` (no `choices=`) and `emit_data_migration.py` (heuristic miss) undetected**, and would land in a committed migration file unless someone separately runs `test_db_integrity.py` — which I confirmed **does** catch it (`B03: doi_resolution_outcome values (12 examined) — 1 invalid values`, PART 4) because it queries live values with a real `NOT IN (...)`, not a regex over SQL text. Net effect: the guard that is supposed to sit at the point of emitting the migration is weaker than documented; the guard that actually works sits one stage later, against the rebuilt DB.

### 19. `add-population-match` on a **same-session** dissenting grade — **crashes instead of landing as the documented second row** (task 5)
See PART 3, case 26 — logged there since it's the population-match writer, not `add-source`.

### 20. `add-source` cannot set `--co1-provenance`/`--co1-source-type` at all — **the CLAUDE.md §6 Co-1 failure, reproduced** (task 4)
See PART 5, case 24-25.

### 21. Cross-check: `add-locator` correctly refuses the mirror-image duplicate
INVOKED: `add-locator --ref-id REF-00975 --doi 10.1080/10400435.1997.10132293 --recovered-from smoke-test-2026-08-25 --status REFERENCE-ONLY ...` (REF-00971's DOI, held in `evidence_sources` only).
EXIT: 1. `ValueError: DOI '10.1080/10400435.1997.10132293' is already held as REF-00971 in evidence_sources. R9: cross-file the existing ref_id, never mint a second identity for one source.`
FINDING: PASS — confirms `insert_locator`'s two-table check (case 11's contrast) is real and symmetric in the direction it does cover. LOCATION: `scripts/db.py:2513-2521`.

**PART 2 EXAMINED total: 15 refusal/acceptance probes against `add-source`/`add-locator`. 13 behaved as documented; 2 are real gaps (tier range, doi_resolution_outcome enum) both closed one-to-two stages downstream; 1 (OD-5, case 11) is a live, un-mitigated defect at the exact writer a real batch would use most.**

---

## PART 3 — R13 population matching / divergent grades (task 5)

### 22. `add-population-match` — real grade, real mobility population
INVOKED: `add-population-match --ref-id REF-00971 --target-population MOB --study-population "wheelchair and walker users, mobility-impaired sample (Sanford et al 1997)" --sample-size 30 --match-grade EXACT --session $SESSION`
EXIT: 0. `{"match_id": "session_2026-08-25-pipel-REF-00971-MOB", ...}`. FINDING: PASS. LOCATION: `scripts/db.py:2308-2360`.

### 23. FK refusals on `add-population-match` (read, not separately re-run — code-verified)
`ref_id` must be an admitted source (`scripts/db.py:2317-2321`) and `target_population` must exist in `populations` (`scripts/db.py:2322-2324`); `match_grade` is CHECK-enforced (`evidence_population_match.match_grade IN ('EXACT','PARTIAL','PROXY','MISMATCH')`) and `MISMATCH` additionally requires `--mismatch-note` (`scripts/db.py:2327-2330`). FINDING: PASS (design read directly from source, consistent with every other writer in this file).

### 24. **Divergent grade, same session — crashes on a PK collision instead of landing as documented**
INVOKED: same `--ref-id REF-00971 --target-population MOB`, different `--match-grade PARTIAL`, **same** `--session $SESSION`.
EXIT: 1. Prints the intended NOTE first (`NOTE: REF-00971 x MOB already graded by [...]. Writing a second row -- divergent grades read as a contest...`) then crashes: `sqlite3.IntegrityError: UNIQUE constraint failed: evidence_population_match.match_id`.
FINDING   : **FAIL — the documented mechanic is broken for the most natural case (re-grading within one working session).**
LOCATION  : `scripts/db.py:2355-2356` — `match_id` auto-derives as `f"{session[:24]}-{ref}-{target_population}"` whenever `--match-id` isn't supplied, and **`add-population-match`'s argparse block (`scripts/db.py:839-849`) has no `--match-id` flag at all** — there is no way to give the second row a distinct id from the CLI. `match_id` is the table's `PRIMARY KEY`.
NOTE      : CLAUDE.md §4 correctly states there is **no uniqueness constraint on `(ref_id, target_population)`** — true at the schema level, verified. But the CLI's own deterministic id derivation reintroduces a **de facto** one-row-per-session limit that the doctrine doesn't intend, and the failure mode is an unhandled `IntegrityError` traceback, not a graceful `ValueError` in the house style used everywhere else in this file.

### 25. Divergent grade, **different session** — works exactly as documented
INVOKED: same call, `--session session_2026-08-25-adversarial-recheck-mobility-smoke`.
EXIT: 0. `{"match_id": "session_2026-08-25-adver-REF-00971-MOB", ...}`.
OUTPUT: both rows now persist —
```
('session_2026-08-25-pipel-REF-00971-MOB', 'EXACT',   'session_2026-08-25-pipeline-smoke-test-mobility')
('session_2026-08-25-adver-REF-00971-MOB', 'PARTIAL', 'session_2026-08-25-adversarial-recheck-mobility-smoke')
```
FINDING: PASS — the "second row, distinguished by created_by_session" mechanic is real, across sessions.

### 26. What reads the divergence? — **ABSENT**
INVOKED: `grep -rn "v_divergence\|GROUP BY.*ref_id.*target_population\|COUNT(DISTINCT match_grade)" scripts/ governance/`
FINDING   : **ABSENT.**
LOCATION  : `v_divergence` (`scripts/migrations/057_baseline_2026-08-12.sql:6562-6567`) is a **false friend** — it joins `specifications`/`convergence_assessment` at the **synthesis** stage and has nothing to do with `evidence_population_match`. Every script that touches `evidence_population_match` (`scripts/audit/research_batch_dod.py`, `scripts/audit/research_protocol_audit.py`, `scripts/validate_population.py`) either counts total matches, tallies `match_grade` globally, or checks coverage (≥1 row per ref) — **none does `GROUP BY (ref_id, target_population) HAVING COUNT(DISTINCT match_grade) > 1`** to surface a contest. `population_integrity_audit.py` (task 7) doesn't touch this table at all — it checks a different, judgment/synthesis-stage population-linkage layer (`citation_population_links`, `probe_population_links`, `extraction_population_links`, all 0 rows).
NOTE      : The write-side half of the adversarial-dissent mechanic (task 5's premise) is real and demonstrated in case 25. **The read side that would make a dissent visible to anyone does not exist.** Two divergent grades sit in the table indistinguishable, to any consumer, from an accidental duplicate.

---

## PART 4 — Author fidelity, tier/scope, and the blocking gate (tasks 4 continued, and the headline finding)

### 27. `retrieval_log.py --verify-authors` against the **canonical** DB's existing 10 sources (read-only, no scratch)
INVOKED: `python3 scripts/research/retrieval_log.py --verify-authors --session session_2026-08-19-research-batch-01-room-acoustic-performance` and again for `session_2026-08-22-research-batch-02-room-acoustic-performance` (the two sessions holding logged payloads for the corpus's 10 live sources).
STAGE: evidence-collection. EXIT: 0/0. RUNTIME: <1s each, no network (`data/guidebook.db` opened `mode=ro`; the two hard prohibitions — no writes, sha256 unmoved — hold: verified before/after).
READS: `retrieval-log/session_2026-08-19-.../manifest.jsonl` (5 payloads) and `retrieval-log/session_2026-08-22-.../manifest.jsonl` (7 payloads, 5 DOI-bearing not already covered by the first).
EXAMINED: 5 + 5 = **10 of 10** live `evidence_sources` rows, split across the two sessions that produced them.
OUTPUT: both `CLEAN`.
FINDING: PASS. LOCATION: n/a.
NOTE: **`author_fidelity` (the registered check, `governance/check-registry.yaml:729-744`) has a real, currently-clean subject on the canonical corpus.** It is `level: advisory`, keyed to `session_pointer: LATEST-RESEARCH`. `sessions/LATEST-RESEARCH` currently reads `session_2026-08-22-research-batch-02-room-acoustic-performance.md` (unchanged by this smoke test, since I never touched it per PROTOCOL). **It would have a subject for a fresh mobility admission only if that batch (a) logs its retrieval under the tracked `retrieval-log/<session>/` tree — not scratch, as I deliberately did here — and (b) updates `sessions/LATEST-RESEARCH` to point at itself.** Both are real, load-bearing, undocumented-in-the-flag prerequisites; my own REF-00971 admission is invisible to the registered check right now, by design (rule 3 compliance), which is itself proof the pointer is load-bearing and not automatic.

### 28. Co-1 admission with no `co1_provenance`/`co1_source_type` — **CLAUDE.md §6's exact failure, mechanically reproduced** (task 4)
INVOKED:
```
python3 scripts/db.py add-source --ref-id Co1-99 --author "corp|[SMOKE-TEST PLACEHOLDER ORG - not real evidence]" \
  --year 2026 --title "[SMOKE-TEST PLACEHOLDER] Co-1 admission with NO co1_provenance/co1_source_type - proving CLI cannot set them" \
  --tier 1 --evidence-type co1 --metadata-quality GREY --verification-status UNVERIFIED --session $SESSION
```
EXIT: 0. `{"ref_id": "Co1-99", ...}`.
FINDING   : **FAIL — this is the worst failure class CLAUDE.md §6 names, mechanically possible today.**
LOCATION  : `schemas/evidence_source.py:130-159` (`co1_field_consistency`) is a **Pydantic validator that enforces exactly this rule** ("Co-1 source requires co1_provenance field (A5 §6.1)") — but `scripts/db.py` **never imports `schemas/evidence_source.py` or invokes Pydantic validation at write time** (confirmed: `grep "import.*evidence_source\|from schemas" scripts/db.py` → no matches). Worse: **`add-source`'s argparse block has no `--co1-provenance`/`--co1-source-type` flag at all** (`co1_provenance`/`co1_source_type` appear only in the internal `_ES_COLS` whitelist, `scripts/db.py:1902`, reachable only via the Python API, never the CLI).
OUTPUT (verified row): `{'ref_id': 'Co1-99', 'evidence_type': 'co1', 'tier': 1, 'co1_provenance': None, 'co1_source_type': None, 'verification_status': 'UNVERIFIED'}`
NOTE      : A Co-1 source can be filed through the sanctioned, documented CLI with its co-production provenance permanently null and nothing refuses it — the schema-level rule exists, is well-specified, and is completely disconnected from the write path. This is the single most doctrine-critical gap found in this run.

### 29. Blocking `test_db_integrity.py` against the scratch DB, post-admission
INVOKED: `GUIDEBOOK_DB_PATH=$SMOKE/s2-evidence.db python3 scripts/tests/test_db_integrity.py`
STAGE: evidence-collection (this gate is the blocking backstop for everything above). EXIT: 1 (script exits nonzero on any failed sub-check). RUNTIME: ~2s.
READS: scratch DB only, read-only-shaped queries.
WRITES: NONE.
EXAMINED: **1999 subject-inspections across 46 instrumented checks of 70; 66/70 sub-checks passed.**
OUTPUT (failures):
```
[✗] B03: doi_resolution_outcome values          (12 examined) — 1 invalid value   [my REF-00973 probe, case 18]
[✗] B11: evidence_sources.tier upper bound       (14 examined) — 1 row tier>6      [my REF-00972 probe, case 17]
[✗] I1:  no source is VERIFIED with effort owed  (11 examined) — 1 row VERIFIED without CLOSED disposition
[✗] C07: value columns hold values, not prose    (90 examined) — 1 placeholder-prose row [my own Co1-99, deliberately marked]
```
FINDING   : **B03/B11 are PASS-two-stages-later confirmations of cases 17-18 (expected). C07 is my own deliberately-marked test data being correctly caught (expected, self-inflicted, not a repo defect). I1 is a genuine, unprompted defect surfaced by my ONE real, honestly-sourced admission.**
LOCATION  : **I1 — `scripts/tests/test_db_integrity.py:312-318`** (`WHERE verification_status='VERIFIED' AND COALESCE(verification_disposition,'') <> 'CLOSED'`) fires on **REF-00971**, my real Sanford/Story/Jones admission, because `scripts/db.py:1961-1976` (`insert_evidence_source`'s VERIFIED/UNVERIFIED branch) **only ever defaults `verification_disposition` in the UNVERIFIED branch (`data.setdefault("verification_disposition", "OPEN")`, line 1975) — the VERIFIED branch never sets it**, and **`add-source` exposes no `--verification-disposition` flag at all** (confirmed: `grep "verification.disposition" scripts/db.py` → only the two lines already cited).
NOTE      : **This is the headline finding of the whole run.** Every single step of the documented, honest admission path — real search, real Crossref retrieval with a logged artefact, real DOI-resolution cross-check, correctly-populated `verification_method='tool'`/`verified_by_tool='crossref'`, `metadata_quality='COMPLETE'` — produces a row that **cannot pass the blocking integrity gate CLAUDE.md §4 itself names as the verification step** ("Verify with `migrate_db.py --rebuild ...`"), on the very first use, through no fault of the researcher. A real mobility batch following the documented path exactly will hit this on its first VERIFIED admission.

---

## PART 5 — `evidence_type`/`scope` vocabulary: the second headline finding

### 30. `adjudication_integrity.py` against the scratch DB, post-admission
INVOKED: `GUIDEBOOK_DB_PATH=$SMOKE/s2-evidence.db python3 scripts/audit/adjudication_integrity.py`
EXIT: 0 (script reports VERDICT: FAIL in its text but does not set a nonzero process exit — noted as its own minor defect). RUNTIME: <1s.
EXAMINED: 12 (of 15 evidence_sources rows — those with non-null evidence_type).
OUTPUT:
```
[1] FAIL: 2 tier-derivation inconsistency(ies) of 12 checked:
    Co1-99: (co1, None) stored tier 1 — underivable: no ratified tier for (evidence_type='co1', scope=None); valid scopes for this type: ['intrinsic']
    REF-00971: (empirical, None) stored tier 1 — underivable: no ratified tier for (evidence_type='empirical', scope=None); valid scopes for this type: UNKNOWN evidence_type
```
FINDING   : **FAIL, and the REF-00971 line is the important one** — `Co1-99` failing is expected (case 28's placeholder never got a real `scope` either, consistent with that finding). **REF-00971 is my real admission, and it fails for a different, structural reason: `evidence_type='empirical'` is not a ratified value at all.**
LOCATION  : `schemas/tier_derivation.py:49-59` — the ratified `evidence_type` vocabulary is exactly `{clinical, co1, sr_meta, standard_eb, co2, grey, national_fw, code}`. `'empirical'` (what I typed, and what `db.py` silently accepted — see case 31) is not one of them. The correct value for a controlled human-subjects biomechanical/intervention study — which is explicitly this paper's shape and is named verbatim in `schemas/tier_derivation.py:12-16` ("intervention / RCT / biomechanical / sensory-threshold studies") — is `clinical`, with `scope='high_control'` (→ Tier 1, matching what I set).
NOTE      : I made this exact mistake in real time, following the CLI's own (unenforced) `--evidence-type` free-text field, and only discovered it by running this audit — precisely the scenario CLAUDE.md §2(a)/§2(c) exist to catch.

### 31. Why `db.py` let `evidence_type='empirical'` through — and the fix already exists elsewhere in the same file
INVOKED: `grep -n check_vocab scripts/db.py` (no hit for `evidence_type` on the `add-source` path) vs. `scripts/db.py:1223-1224` (`add-supersession-check`'s `--evidence-type` **does** carry `choices=["clinical","co1","co2","sr_meta","standard_eb","national_fw","code","grey"]` — the exact ratified list).
Reproduced directly: `add-supersession-check --evidence-type empirical ...` → `error: argument --evidence-type: invalid choice: 'empirical' (choose from 'clinical', 'co1', 'co2', 'sr_meta', 'standard_eb', 'national_fw', 'code', 'grey')` (EXIT 2) — then `add-supersession-check --evidence-type clinical ...` → succeeds (`{"check_id": "SUPCHK-5a693c37feb8", ...}`).
FINDING   : **FAIL on `add-source`; the fix is a two-line diff away, since `add-supersession-check` (`scripts/db.py:1223-1224`) already carries the correct `choices=` list in the same file.**
LOCATION  : `scripts/db.py:1085` (`p_as.add_argument("--evidence-type")` — no `choices=`) vs. `scripts/db.py:1223-1224` (same file, correct enforcement).
NOTE      : This is not a missing feature that needs designing — the constraint is already written, correctly, twenty lines away in spirit and needs only to be copied onto the one command that admits sources in the first place.

### 32. `scope` cannot be set through the sanctioned write path **at all**
INVOKED (Python API, since there is no `--scope` CLI flag to even attempt):
```python
db.insert_evidence_source({'ref_id':'REF-00976','year':2020,'title':'scope test','tier':1,
    'evidence_type':'clinical','scope':'high_control'}, session=SESSION, authors=[...])
```
EXIT: raised (caught). OUTPUT: `ValueError: insert_evidence_source: unknown column(s) {'scope'}. Permitted: frozenset({...23 columns, no 'scope'...})`
FINDING   : **FAIL — the strongest single finding in this run.**
LOCATION  : `evidence_sources.scope` (`scripts/migrations/...` — column carries `CHECK (scope IS NULL OR scope IN ('high_control','lower_control','national','international','intrinsic'))`, matching `schemas/tier_derivation.py`'s `ALL_SCOPES` exactly) is **absent from `_ES_COLS`, the whitelist `insert_evidence_source` validates against (`scripts/db.py:1892-1915`)**, and **`add-source`'s argparse block has no `--scope` flag** (confirmed: `grep -- "--scope" scripts/db.py` → no hits anywhere in the file).
NOTE      : Per `schemas/tier_derivation.py`, `scope` is **required** to derive a tier for any `clinical` or `standard_eb` source — the two evidence types that cover essentially all primary research and named national/international standards, i.e. the bulk of what a real mobility batch would admit. **Every source of these two types admitted through `db.py add-source` is therefore structurally guaranteed to fail `adjudication_integrity.py`'s tier-derivation check the moment it is written**, because there is no way, through the sanctioned CLI or its underlying Python API's own column whitelist, to populate the one column that makes the derivation possible. A committed migration (`data_20260822012400_2026-08-22-record-correction-and-biblio-repair.sql:20`) shows this already happened once for real, for the 5 room-acoustic sources, and required a hand-written follow-up `UPDATE ... SET scope=...` outside the sanctioned pipeline to fix — the migration's own commit message names the mechanism: *"scope was NULL on all five sources, which made every stored tier UNDERIVABLE... SCOPE RECORDED 2026-08-22"*. That repair pattern is guaranteed to recur for a mobility batch, by construction, until `--scope` exists on `add-source`.

---

## PART 6 — Stage-specific writers: `add-jurisdictional-value`, `add-economics-entry`, `add-case-study`, `add-locator` (task 6)

### 33. `add-jurisdictional-value` — refusals, real mobility item (E-03, ramp gradient)
Five probes, all against `item_code=E-03`:
- unknown `item_code` (`Z-99`) → `ValueError: item_code 'Z-99' is not in items.` (`scripts/db.py:2373-2374`) — PASS
- `--evidence-tier 9` → `ValueError: evidence_tier 9 is outside the ratified 1-6 band (RANGE_GUARDS...)` (`scripts/db.py:2379-2382`) — PASS
- `--value-numeric 14` with no `--unit` → `ValueError: --value-numeric requires --unit. A number without a unit is not a value.` (`scripts/db.py:2388-2390`) — PASS
- quantified value, no locator, no `[UNVERIFIED-QUANT]` marker → **R3 refusal**: `ValueError: R3: a quantified code value needs a locator (clause/section/page) or an explicit [UNVERIFIED-QUANT] marker in --notes. Nothing written.` (`scripts/db.py:2383-2394`) — PASS, this is the task's named R3 test
- same value **with** `[UNVERIFIED-QUANT]` marker, honestly noting I have no retrieved locator this session → EXIT 0, `jv_id=110` written (`jurisdictional_values` @ E-03/AU/AS 1428.1, value_numeric=14, unit='ratio-1-in-N') — PASS
EXAMINED: 5 probes. FINDING: PASS on all five — R3 behaves exactly as documented, and (deliberately, per PROTOCOL rule 4 and CLAUDE.md's citation discipline) I did not fabricate a locator for a code clause I have not actually retrieved this session; I used the honest `[UNVERIFIED-QUANT]` escape instead. Pre-existing corpus context: `jurisdictional_values` already held 8 rows for E-03 (US/GB/DE/AU/NO/FR/CH/ISO) all with `value_numeric IS NULL` — confirming this is a genuine, real gap a mobility batch would need to fill, not a hypothetical.

### 34. `add-economics-entry` — pointer discipline (rule 5) live-tested
`--year`/`--journal` **flags do not exist** on the CLI at all (`scripts/db.py:869-883`); reachable only via the Python API, where they are explicitly refused when `--ref-id` is given:
```
db.insert_economics_entry({..., 'ref_id':'REF-00971', 'year':1997, 'journal':'Assistive Technology', ...})
# ValueError: --ref-id was given, so ['year', 'journal'] are reachable through it and must
# not be copied onto this row (CLAUDE.md rule 5: point, do not copy)...
```
Then, real-shaped success with `ref_id` given and no restated fields → `entry_id='ECON-SMOKE-01'` written. FINDING: PASS. LOCATION: `scripts/db.py:2419-2439` (the refusal is explicitly commented as "verified 2026-08-25 by calling insert_economics_entry directly; through argparse it is unreachable, and that is the point, not an oversight" — I independently reproduced exactly that).

### 35. `add-case-study` — `--sources` refuses a bare `REF-NNNNN`
`--sources "REF-00971"` → `ValueError: --sources contains a REF-NNNNN. A reference id in a prose field is a flattened pointer (CLAUDE.md rule 5). Link the source through case_study_specs / the evidence tables, and keep --sources for material that has no ref_id.` FINDING: PASS. LOCATION: `scripts/db.py:2476` region.

### 36. `add-locator` — `--recovered-from` required, then real success + both dupe directions
`--recovered-from` missing → argparse error (EXIT 2). With it supplied: DOI dup vs. `evidence_sources` refused (case 21, cross-referenced); a genuinely new lead (`REF-00975`, unrelated DOI, explicitly titled "Lead:...(unretrieved, clue-store only)") admitted cleanly, EXIT 0. FINDING: PASS.

**PART 6 EXAMINED total: 4 writers, 11 real invocations, all behaving exactly as designed — no new defects in this part beyond the OD-5/evidence_type/scope findings already logged above.**

---

## PART 7 — Evidence-stage gates (task 7)

All run with `GUIDEBOOK_DB_PATH=$SMOKE/s2-evidence.db`.

| Script | EXIT | EXAMINED | Verdict | Note |
|---|---|---|---|---|
| `scripts/audit/metadata_integrity_audit.py` | 0 | **15** | PASS | Real subject; 11/15 eligible rows lack a cross-check record (pre-DR-2026-05-20 legacy, reported not failed) |
| `scripts/audit_evidence_metadata.py` | 0 | **106** (slugs) | PASS | Correctly flags my own `Co1-99` placeholder under "VERIFIED but incomplete metadata" — the audit works |
| `scripts/audit/alias_provenance_audit.py` | 0 | **2382** aliases | PASS | Substrate-table (`term_aliases`), not evidence-collection per se, but explicitly in my task list. 880 grandfathered pre-provenance rows; AR/BN/HI/SW flagged as structurally unsearchable (no aliases at all) |
| `scripts/audit/source_slug_links_duplicates.py` | 0 | **11** | PASS | Real subject: my new REF-00971↔slug link included, 0 duplicate (slug, local_ref_id) sets |
| `scripts/audit/population_integrity_audit.py` | 0 | **0** | **VACUOUS** | Checks `citation_population_links`/`probe_population_links`/`extraction_population_links` — a judgment/synthesis-stage linkage layer, **not** `evidence_population_match`. All three tables are 0 rows on this DB. My new `evidence_population_match` rows (cases 22-25) are invisible to this specific audit — it doesn't query that table at all |
| `scripts/audit/adjudication_integrity.py` | 0* | **12** | **FAIL** | See PART 5, case 30. *Script prints `VERDICT: FAIL` but its process exit code is 0 — a minor defect: a caller scripting on exit code alone would miss this |
| `scripts/tests/test_db_integrity.py` | 1 | **1999 across 46 checks (66/70 sub-checks pass)** | **FAIL** | See PART 4, case 29 — the blocking gate itself, exercised end-to-end |
| `scripts/validate_population.py` | 0 | **425** | PASS | Confirms my `evidence_population_match` writes used a valid population code (MOB) |
| `scripts/validate_jurisdiction.py` | 0 | **111** | PASS (55 warnings) | Checks `references/standards-registry.md` + `data/sources/`, a **markdown registry**, not the `jurisdictional_values` SQL table — my new jv_id=110 row is not examined by this validator at all |
| `scripts/validate_verification_consistency.py` | 0 | **0** | VACUOUS, by decision | Checks `specifications` (judgment-stage table, empty pre-Phase-E) — correctly reported "empty by decision" per the registry note, not a defect |

**PART 7 EXAMINED total across 10 gates: 4934 subject-inspections. 2 genuinely VACUOUS (one by legitimate design, one because the gate checks a different table than the one this stage's mobility batch would actually populate). 2 FAIL, both already logged as headline findings in PART 4/5.**

---

## PART 8 — Evidence-stage skills (task 8)

| Skill | Named script(s) | Exists? | Runs? | Teaches hand SQL? | Wired to sanctioned write path? |
|---|---|---|---|---|---|
| `citation-verifier` | none (prose protocol) | n/a | n/a — pure procedure using PubMed/Consensus/Scholar Gateway connectors | No | **No — see finding below** |
| `evidence-auditor` | `scripts/db.py add-gap`, `gaps --status OPEN` | yes | yes (exercised via PART 2/6 above) | No | Yes |
| `bibliography-compiler` | `scripts/db.py coverage --slug {slug}` | yes | yes | No | Yes |
| `evidence-metadata-rehabilitation` | `scripts/audit/metadata_integrity_audit.py`, `scripts/audit_evidence_metadata.py` | yes, yes | yes, yes (PART 7) | No | Yes |
| `cross-reference-resolver` | none — narrative §/Part/Appendix cross-refs | n/a | n/a | No | **N/A — this is a render-stage skill, not evidence-collection**, despite being in my assignment list |
| `relational-integrity-checker` | SQLite queries over item/population/slug codes across gap register, connection register, BPC, Part 4 | implicit, not a fixed script | not separately run | No | Substrate/cross-cutting, not evidence-collection-specific |
| `supersession-audit` | `scripts/db.py add-supersession-check`, `update-bpc` | yes | yes (PART 5, cases 30-31; the ratified `--evidence-type choices=` live here) | No | Yes |
| `multilingual-research` | `scripts/db.py coverage`, `is-mined`, `log-mining` | yes | not separately re-run (S1's territory; `db.py is-mined`/`log-mining` are research-stage, not evidence-collection) | No | Yes for what it does cover; R11 ("no back-translation") is actually defined in `research-log-manager` (a **different** skill), not in `multilingual-research` itself |
| `integrity-protocol` | `scripts/preflight.sh`, `register_integrity_check.py`, `matrix_consistency.py`, `claims_docket.py` | yes | not separately re-run (repo-wide battery, out of this stage's narrow scope) | No | Yes |

### 37. `citation-verifier` — FINDING: **the skill is not wired to the sanctioned SQLite write path at all**
The skill's core body and its HARVEST mode produce **markdown tables** ("BPC Key sources metadata table", `references/bpc/*.md` — a live, populated pattern: 132 files repo-wide carry a "Key sources" section). Its ENRICH mode explicitly instructs querying PubMed/CrossRef and assembling rows in that markdown table format, entirely independent of `scripts/db.py add-source`, `scripts/research/retrieval_log.py`'s artefact discipline, or any of the R9/R10/R3 refusals exercised throughout this log.
FINDING   : **ABSENT / risk** — this is not what the skill was asked to do wrong, it is a genuine wiring gap: an agent following `citation-verifier` ENRICH mode literally for a real mobility batch would retrieve real bibliographic data, write it into a narrative markdown table, produce **no retrieval-log artefact**, go through **none** of the `db.py add-source` refusals (R9 dedup, VERIFIED/method consistency, ref-id shape), and create a **second, unpointed home for bibliographic facts** outside `evidence_sources` — precisely the dual-write CLAUDE.md rule 5 forbids, in a skill file that predates (per its own docstring, "CO-0006 2026-04-08") the SQLite-centric write path CLAUDE.md §4 now mandates.
LOCATION  : `skills/citation-verifier_SKILL.md:93-123` (ENRICH mode).
NOTE      : Whether `references/bpc/*.md` "Key sources" tables are meant to be **generated from** `evidence_sources` (in which case this skill is stale and should be retired/rewired) or are a genuinely separate render-stage artifact was not resolvable from this stage's scope — flagged for a render-stage (S5) or synthesis-stage read, not resolved here.

---

## PART 9 — Verification artefact discipline (task 9)

### 38. Structure of `retrieval-log/`
INVOKED: `ls -la retrieval-log/*/` (tracked tree, read-only)
FINDING: PASS — matches `scripts/research/retrieval_log.py`'s design exactly: one directory per session, `manifest.jsonl` (one line per fetch: url, purpose, sha256, bytes, exit, artefact filename) plus the raw response bytes named by sha256 prefix + sniffed extension.
EXAMINED: 3 tracked session directories (`session_2026-08-19-research-batch-01-room-acoustic-performance`, `session_2026-08-20-provenance-walk`, `session_2026-08-22-research-batch-02-room-acoustic-performance`).

### 39. Would a fresh mobility admission produce one? — proven yes, mechanically (case 2 above)
Already demonstrated end-to-end in PART 1, case 2: `retrieval_log.fetch()` wrote the payload to disk **before** returning it to the caller (`scripts/research/retrieval_log.py:118-131`, write happens ahead of the `return`), and the sha256 of what was written matched an independently-made `curl` of the same URL byte-for-byte. FINDING: PASS.

### 40. Offline diff path, proven
`--verify-authors` (case 6 and case 27) reads **only** the manifest + artefact files and the DB — zero network calls during verification itself, confirmed by running it successfully with the scratch/log environment variables pointed entirely at local paths after the fetch had already happened. FINDING: PASS — "verification must leave an artefact" (CLAUDE.md §2(c)) is a real, working mechanism, not aspirational; I both created a fresh artefact and diffed it offline in the same run.

---

## PART 10 — Extraction: the evidence→judgment hinge (task 10)

### 41. `source_value_extractions` — no writer exists anywhere
INVOKED: `grep -rn "INSERT INTO.*source_value_extractions" scripts/` → **zero matches**, anywhere in the tree (migrations' `CREATE TABLE`/`ALTER TABLE` aside). Cross-checked against the full `db.py` subcommand list (37 subcommands enumerated from `sub.add_parser` — `migrate`, `gaps`, `connections`, `is-mined`, `log-mining`, `add-candidate`, `add-population-match`, `add-jurisdictional-value`, `add-economics-entry`, `add-case-study`, `add-locator`, `next-id`, `coverage`, `synonyms`, `add-gap`, `close-gap`, `add-connection`, `update-connection`, `unmined`, `upsert-coverage`, `upsert-language`, `log-search`, `update-bpc`, `add-source`, `add-conflict`, `update-conflict`, `conflicts`, `delete-connection`, `add-item`, `items`, `add-audit-run`, `update-audit-run`, `audit-runs`, `add-supersession-check`, `add-gap-mining`, `update-gap-addressability`, `unmined-gaps`) — **no `add-extraction` or equivalent**.
FINDING   : **ABSENT.**
LOCATION  : `source_value_extractions` (schema at `scripts/migrations/057_baseline_2026-08-12.sql` + later `ALTER`s) is READ by `scripts/assess/assess_cell.py`, `scripts/generate/pilot_renderings.py`, `scripts/audit/adjudication_integrity.py`, `scripts/audit/population_integrity_audit.py`, `scripts/tests/test_db_integrity.py` — five consumers, zero producers.
NOTE      : The schema itself is well-designed and clearly built with exactly this project's mobility corpus in mind — `device_class IN ('manual_self_propelled','manual_attendant','power_chair','scooter','bariatric_manual','bariatric_power','walker_rollator','mixed','not_device_scoped')` and `measurement_paradigm IN ('swept_path_dynamic','static_turning_circle','static_clearance','anthropometric_percentile','instrumented_physical_measurement','route_metric','field_observation','participatory_spatial','stated_unmeasured')` are precisely the categories a corridor-width or turning-space extraction from a wheelchair anthropometry study (e.g. REF-00971's ramp-slope data, or the Anthropometry of Wheeled Mobility Project already sitting as a lead at `source_locators` REF-00468) would need. **None of it is reachable.** A real mobility batch that retrieves a source containing an actual corridor-width or ramp-gradient figure has a sanctioned way to admit the SOURCE (`add-source`), link it to a SLUG (`source_slug_links`), and grade its POPULATION match (`add-population-match`) — but **no sanctioned way to record the extracted VALUE itself**, its locator, or its link to an `item_code`. This is the exact stated hinge to the judgment stage (`root_ref_id REFERENCES evidence_sources`, `promoted_to_rdc_id REFERENCES reasoning_doc_citations`, `item_code REFERENCES items`), and it is unbuilt on the write side. `adjudication_integrity.py`'s own `assess_source()` (`scripts/assess/assess_cell.py:196-202`) hardcodes the value dimension as `NOT_ASSESSED` and says so explicitly in a comment: *"still absent is any assessment RULE for grading a value dimension from them — writing one is a judgment act, not a caller sweep."*
Minor, separate finding in the same area: that same comment (`scripts/assess/assess_cell.py:196-198`) asserts `source_value_extractions` "holds 8 rows as of migration 052" — **stale**; the live table holds 0 rows on both the canonical DB and this scratch copy, almost certainly because the 2026-08-06 clean-room reset (referenced in `governance/check-registry.yaml:264-267`) reset it along with `evidence_sources` (863→10 rows). A small, live instance of CLAUDE.md §2(b)'s exact failure (a hardcoded fact drifting in a code comment), flagged for whoever owns that file next — not chased further here as it's a comment, not a live gate.

---

## S2 SUMMARY

### (a) Verdict table

| Component | Kind | Verdict | Key evidence |
|---|---|---|---|
| `add-source` real admission | writer | PASS mechanically / **FAIL downstream** | REF-00971 written correctly, then fails I1 (PART 4) and tier-derivation (PART 5) |
| `add-source` R9 dupe (within `evidence_sources`) | refusal | PASS | case 10 |
| `add-source` R9 dupe (vs `source_locators`, OD-5) | refusal | **FAIL — live defect** | case 11 |
| `add-source` VERIFIED/method/tool consistency | refusal | PASS | cases 12-13 |
| `add-source` ref-id shape | refusal | PASS | case 8 |
| `add-source` tier range | refusal | FAIL at write time, PASS 2 stages later | case 17 |
| `add-source` doi_resolution_outcome enum | refusal | FAIL at write + emit time, PASS at test_db_integrity | case 18 |
| `add-source` evidence_type vocabulary | refusal | **ABSENT (unenforced), fix exists 20 lines away** | cases 30-31 |
| `add-source` scope column | writer coverage | **ABSENT entirely** | case 32 |
| `add-source` co1_provenance/co1_source_type | writer coverage | **ABSENT entirely** | case 28 |
| `add-source --dry-run` + `--slug` | writer | **FAIL — crashes** | case 4 |
| `add-locator` R9 dupe (both directions) | refusal | PASS | cases 11 (contrast), 21, 36 |
| `add-population-match` divergent grade, same session | writer | **FAIL — crashes on PK collision** | case 24 |
| `add-population-match` divergent grade, cross-session | writer | PASS | case 25 |
| divergence surfaced to a reader | consumer | **ABSENT** | case 26 |
| `add-jurisdictional-value` (R3, tier range, item FK) | writer | PASS | case 33 |
| `add-economics-entry` (rule-5 pointer discipline) | writer | PASS | case 34 |
| `add-case-study` (`--sources` REF- refusal) | writer | PASS | case 35 |
| `retrieval_log.py --verify-authors` | verifier | PASS, real subject both on canonical and fresh admission | cases 6, 27 |
| `retrieval-log/` artefact discipline | mechanism | PASS | cases 38-40 |
| `test_db_integrity.py` (blocking) | gate | Real subject, correctly catches 4/4 induced+organic defects | case 29 |
| `adjudication_integrity.py` | gate | Real subject, correctly catches the scope/evidence_type gap; **exit code doesn't reflect its own FAIL verdict** | case 30 |
| `population_integrity_audit.py` | gate | **VACUOUS** for this stage's actual writes (checks a different table) | PART 7 |
| `validate_jurisdiction.py` | gate | Real subject, **but not the SQL table this stage writes to** | PART 7 |
| `metadata_integrity_audit.py`, `audit_evidence_metadata.py`, `source_slug_links_duplicates.py`, `validate_population.py` | gates | PASS, real subjects | PART 7 |
| `citation-verifier` skill | skill | **Not wired to the sanctioned write path; risks a second, unpointed home for bibliographic facts** | case 37 |
| `evidence-auditor`, `bibliography-compiler`, `evidence-metadata-rehabilitation`, `supersession-audit` skills | skill | Wired correctly, exercised | PART 8 |
| `cross-reference-resolver`, `relational-integrity-checker` skills | skill | Out of this stage's actual scope (render/substrate) despite being assigned | PART 8 |
| `source_value_extractions` writer | writer | **ABSENT entirely — 5 readers, 0 producers** | PART 10 |

### (b) Ranked blockers for a real mobility batch

1. **`evidence_sources.scope` cannot be set by `add-source`, at all** (case 32) — guarantees every `clinical`/`standard_eb` admission fails tier-derivation on write. `scripts/db.py:1892-1915` (whitelist), `scripts/db.py:1085` region (no flag). **Highest priority: this blocks the majority of realistic mobility admissions (primary research + named standards) from ever passing adjudication without a hand-written follow-up UPDATE — the exact anti-pattern CLAUDE.md's write path was built to eliminate.**
2. **`add-source --verification-status VERIFIED` never sets `verification_disposition='CLOSED'`, and there is no `--verification-disposition` flag** (case 29) — guarantees every VERIFIED admission fails the *blocking* `test_db_integrity.py` I1 check. `scripts/db.py:1961-1976`.
3. **`add-source --evidence-type` has no `choices=` enforcement**, though the correct 8-value ratified list already exists verbatim at `scripts/db.py:1223-1224` for a sibling command. `scripts/db.py:1085`.
4. **Co-1 provenance cannot be set through the CLI** (case 28) — the exact CLAUDE.md §6 failure class is currently unmitigated at the write path, though mitigated (unused) in `schemas/evidence_source.py:130-159`.
5. **OD-5 is live**: `add-source`'s DOI dedup check ignores `source_locators`, the project's own 875-row clue store and PROTOCOL's stated driver for this batch (case 11). `scripts/db.py:1992-2000`.
6. **`add-population-match` cannot record a same-session dissenting grade** — crashes on a PK collision instead of landing as documented (case 24), and nothing surfaces a cross-session dissent to a reader even when it does land (case 26).
7. **`source_value_extractions` has no writer** — the evidence→judgment hinge for the actual numeric values (corridor widths, gradients) a mobility batch exists to capture is unbuilt (PART 10).
8. **`add-source --dry-run` combined with `--slug`/`--local-ref-id` crashes** rather than previewing (case 4) — a process-hygiene defect, not data-integrity, but blocks safe rehearsal of the exact call shape a real batch will use.
9. **`add-source` has no `--volume`/`--issue` flags** (case 6) — a `metadata_quality='COMPLETE'` row can never actually be complete for a journal article through this path.

### (c) The ABSENT list

- A `--scope` flag on `add-source` (case 32).
- A `--co1-provenance`/`--co1-source-type` flag on `add-source` (case 28), and any write-time invocation of `schemas/evidence_source.py`'s Co-1 validator.
- A `--match-id` flag on `add-population-match`, needed for the documented same-session dissent mechanic to actually work (case 24).
- Any reader that surfaces divergent `evidence_population_match` grades as a contest (case 26) — `v_divergence` is a false friend (synthesis-stage, unrelated table).
- Any writer for `source_value_extractions`, `extraction_population_links`, `url_verification_runs`, `reference_stubs`, `external_root_registry` — all five 0-row tables in my stage's remit, and I found zero producers for any of them (only `source_value_extractions` has active readers; the other four appear genuinely dormant/pilot-scaffolding).
- `--volume`/`--issue` flags on `add-source` (case 6).
- A skill wiring `citation-verifier`'s ENRICH mode to `db.py add-source` / `retrieval_log.py` instead of a markdown table (case 37).

### (d) Is an honest, fabrication-proof admission mechanically possible today?

**Yes, for the fabrication-proofing specifically — and no, for a clean pass through the pipeline's own downstream gates.**

The 2026-08-19 failure mode itself — an invented author list or a self-asserted "VERIFIED via tool" with no artefact behind it — is now genuinely hard to reproduce: `retrieval_log.fetch()` persists the actual retrieved bytes before the caller ever sees them, `--verify-authors` diffs stored data against that artefact offline, and I reproduced the entire chain end-to-end with a real, independently-verifiable source (byte-identical sha256 across two separate fetches) and got a clean, correct match. **The specific hole that let five fabricated author lists through in the original incident is closed.**

But the write path immediately downstream of that success is not clean: my one real, honestly-sourced, correctly-verified admission (REF-00971) — followed exactly as CLAUDE.md §4 documents, no shortcuts — **fails a blocking integrity check (I1) and an adjudication check (tier-derivation) on its very first write**, for reasons that have nothing to do with the honesty of the sourcing and everything to do with two missing CLI arguments (`--verification-disposition`, `--scope`) and one missing vocabulary constraint (`--evidence-type choices=`, which already exists for a sibling command). A session that follows the documented path exactly, with real, verified evidence, in good faith, will not produce a row that passes CI without a hand-written correction — reintroducing exactly the kind of out-of-band SQL edit the sanctioned write path exists to prevent, on the *first* admission of a new evidence type this project's own doctrine treats as central (T1 clinical/biomechanical primary research, precisely what a mobility batch is built to gather).

---
End time (UTC): 2026-08-25 18:26
