This plan adds no new DEFERRED or PENDING markers. It closes into the run's search logs and its data migration (DR-2026-08-19 §11, properties 4 and 5).

# 11-27 back to work plan: T-104 first run

Session `session_2026-11-28-research-lang-jur-first-run`; branch `ccr-f5fe3b45-3o8ehq`; scratch `/tmp/guidebook-t-104/s.db`. Research only; tooling ships in its own PR (rule 10). Re-derive every figure before trusting it.

## 0. Rule 0 ledger entry (the first write; owner's words only)

Append this to `references/project-standards.md`:

> ## Owner statements 2026-11-28 — research starts; hand fixes are recorded as tooling issues
> "start doing our research across languages and jurisdictions"
> "whatever doesn't work in a session just gets fixed by hand logically within context of project then recorded as a tooling issue to resolve"
> "solving by hand is also a clue for how to solve a tooling problem"
> SUPERSEDES: the 2026-11-27 delegated resolutions' ACTION items 1 and 2 (OD-110), as sequencing only.
> DATE: 2026-11-28 — owner statements, relayed in session and recorded on contact per CLAUDE.md rule 0.

## 1. What the governing query reaches

The governing query reaches REF-00994 and REF-00997, the sources that state parameter 3's shown value. The other six are comparison rows or were never gathered.

## 2. Each source, in order

| Order | Source | Action |
|---|---|---|
| 1 | REF-00997 (AU, governing) | **The only one existing verbs can lift.** Method `direct-render`, no manifest line. Re-retrieve: publisher, then Wayback `if_`. |
| 2 | REF-00994 (governing) | Retrieval logged, but its title is known wrong (GAP-371) and `correct-source` refuses a DOI-less source. **Leave it UNVERIFIED**; VERIFIED over a wrong title breaks integrity. |
| 3 | REF-01016 (NZ, parameters 3 and 12), REF-01013 (Ontario, counts toward CA), REF-01026, REF-01014 | Retrievals logged, but `verification_method` is NULL and not amendable, so VERIFIED is refused. Compare each payload with `pub_title`, `standard_number`, `edition`, `pub_year`, `publisher`; record it with `amend-source --field verification_note`; file the §4 gap. |
| — | REF-01019 | Skip: superseded by REF-01031. |
| — | REF-01002 | Skip: the owner's 2026-09-25 ruling gives up on a source reachable from nowhere, for now. |
| — | REF-01026 as a duplicate | GAP-376 stays open; merging it comes after this run. |

Retrieve REF-00997:

```
python3 -I -c "import sys,sqlite3;sys.path.insert(0,'scripts/research');import retrieval_log as r;u=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True).execute(\"select url from evidence_sources where ref_id='REF-00997'\").fetchone()[0];print(r.fetch(u,'session_2026-11-28-research-lang-jur-first-run',purpose='T-104 re-retrieval',ref_id='REF-00997'))"
curl -sS "http://archive.org/wayback/available?url=des.sa.gov.au/__data/assets/word_doc/0011/21044/"
```

Fetch any snapshot through the same `fetch` call in its `web.archive.org/web/<ts>if_/` form, then once in the plain form.

**If the retrieval succeeds (200 and the payload matches):**

```
GUIDEBOOK_DB_PATH=/tmp/guidebook-t-104/s.db python3 scripts/db.py amend-source --ref-id REF-00997 --field verification_status --replacement VERIFIED --reason "Re-retrieved 2026-11-28; manifest line in retrieval-log/session_2026-11-28-research-lang-jur-first-run" --session session_2026-11-28-research-lang-jur-first-run
```

**If blocked:** keep it UNVERIFIED and append the attempts with `amend-source --field verification_note`. The CHECK's closure reason (`access-denied-persistent`) cannot be written, because `verification_closure_reason` is not amendable; that goes into the §4 gap.

## 3. Research-contract rules that apply

R10 applies: re-retrieve every locator; a block is not final. R8, R9 and R17 have no subject here, because nothing is searched or admitted; they start in §5.

## 4. Gap template for tool failures (a clue for the tooling PR)

```
GUIDEBOOK_DB_PATH=/tmp/guidebook-t-104/s.db python3 scripts/db.py add-gap --category SW --priority P1 --skill run-pipeline --section T-104 --parameter 3 --session session_2026-11-28-research-lang-jur-first-run --description "FAILED: amend-source VERIFIED on REF-01013/01014/01016/01026 refused: verification_method NULL and not amendable (nor verification_closure_reason). WORKAROUND: payload comparison recorded in verification_note; left UNVERIFIED. PROPOSED: amend-source accepts verification_method and verification_closure_reason; correct-source keys DOI-less sources on their ref_id manifest line (closes GAP-044, GAP-371)."
```

Name the gap ids in the commit message and the PR body. The tooling PR (with T-120) ships separately and is replayed before the lifts.

## 5. Next run: languages and jurisdictions

Within OD-04's set, parameter 12 has no figure for US, AU, CA, NO, SE, ISO, EU, CH, NL, DK, FI, IT, JP, KR or CN. Search in `lang_jur_map`'s primary languages (NO/NO, SV/SE, JA/JP, ZH/CN), and log each search before it runs: `db.py log-search --parameter 12 --origin planned --prior-expectation …`. Derive how many `lang_jur_map.scope_status` rows are set: `select count(*), sum(scope_status is not null) from lang_jur_map`.

## 6. Write path

1. `python3 scripts/research/emit_batch_sql.py --scratch /tmp/guidebook-t-104/s.db --out /tmp/guidebook-t-104/batch.sql`
2. `python3 scripts/emit_data_migration.py --session session_2026-11-28-research-lang-jur-first-run.md --summary "T-104 verification" --input /tmp/guidebook-t-104/batch.sql`
3. `python3 scripts/migrate_db.py`, then `python3 scripts/migrate_db.py --rebuild /tmp/guidebook-t-104/rebuilt.db`
4. Commit `retrieval-log/session_2026-11-28-research-lang-jur-first-run/` and run `python3 scripts/preserve_transcripts.py`.
5. Run `/adversarial`, then `/batch-done`, then `scripts/preflight.sh`. Open the PR once and unsubscribe from it.
