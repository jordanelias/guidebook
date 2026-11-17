---
description: The gate that decides whether a research batch is actually finished
---

Never claim a batch is done from your own reading of it. Run the gate the
SessionStart contract names:

```
python3 scripts/audit/research_batch_dod.py --session "$(cat scratchpad/CURRENT)"
python3 scripts/audit/adversarial_pass_audit.py --session "$(cat scratchpad/CURRENT)"
python3 scripts/audit/search_log_completeness.py --session "$(cat scratchpad/CURRENT)"
python3 scripts/audit/refusal_register.py classes --session "$(cat scratchpad/CURRENT)"
```

The second line is RC4 (advisory): it FAILs if this session wrote to any of the 2026-08-19
RULE's research tables and no closed adversarial pass names it. That FAIL is not a reason to
close pass 1; LED-192 holds it open (`/adversarial` step 3). Run it on `CURRENT`, not via
`run_checks.py --all --battery research` — that battery's other session-scoped checks
(`research_dod_session`, `author_fidelity`, `citation_mining_session`) are still pointed
at `LATEST-RESEARCH`, which names the PREVIOUS session for the whole life of this one.

The third line is I5, also on `CURRENT`: it reads the WebSearch/WebFetch ledger the
harness hook wrote and FAILs a WebSearch query that no `search_executions.query_text` of
this session contains — a search you ran and did not log (R8). Log it with
`db.py log-search --backfill 1`: the row is a reconstruction, not a log made as the search
ran, and the `--prior-expectation` it still requires is written after the results, so it
is post hoc and must say so. Its REPORTED lines (unpersisted WebFetch URLs, bare curl/wget
hosts, and web rows logged with no web line on the ledger — a hook that may not have
fired) belong in the session record; they do not fail, and a NOTHING-IN-SCOPE verdict does
not clear them. It witnesses WebSearch and WebFetch only: a search run through an MCP tool
(Consensus, PubMed, Scholar Gateway) leaves no line, so a PASS says nothing about those. R8 still
owes each of them a `log-search` row, and `record_file` its result (DR-2026-09-26 §2.2b); the
gate can check neither.

The fourth line groups every writer refusal this batch met (by signature, verb, stage and cited rule id) and exits 1 while any is undisposed, and a `PROBLEM` line (an unreadable, foreign, duplicated or orphan line) and a `REFUSING` exit (the state graph's `build_graph.py` missing, for example) are red too, not only an undisposed refusal; `refusal_register.py list --session "$(cat scratchpad/CURRENT)"` prints each one with its id. Each is kept in
`scratchpad/<session>/refusals.jsonl` when it was made under the running `--session`: a refusal, a usage error
(an unknown vocabulary term is one: argparse says it and the record keeps it) or a writer's crash. **It exits 2
and prints `NOT RUN` when `scratchpad/CURRENT` does not name an existing `session_YYYY-MM-DD-...` folder** (a
misspelt name, a branch slug, a folder never made): nothing could have been kept there, so nothing was examined, and
that is not a pass. The gate does not run until `CURRENT` is fixed as `/session-open` sets it. An existing folder
with no `refusals.jsonl` is a batch that met none (`EXAMINED: 0`). Not kept: a refusal of a script that takes no
`--session` (`emit_batch_sql.py`) or whose errors are not routed (`migrate_db.py`, `retrieval_log.py`,
`page_image.py`, and `full_text.py`'s `NOTHING TO DERIVE` exit, its several-derivable-files exit and its missing-reader exit): read those on the terminal. Every writer refusal this batch met is disposed before the batch is
done: **retried** (the writer was right; the corrected call succeeded), **parked** (its content waits: file a gap
with `db.py add-gap`, typed by its subject, and keep the refused argv, which is the replay command), or **waived**
(with a reason of at least ten characters). Record each with
`refusal_register.py dispose --session S --id K --as retried|parked|waived [--gap-id G] [--reason R]`, K being the id
`list` prints. `list` checks every disposition again each time it runs: a parked gap that has since been closed puts
the refusal back to UNDISPOSED. An undisposed refusal is a batch that is not done.

For each `CUE` line the fourth line prints, run the named checks once and re-read the named skill section before calling the batch done; say in the pull request what each showed. A refusal in a batch is the sign that the stage it names may not have been performed as the skill says.

**The session id is the bare stem in the DB and carries `.md` in pointer files.**
Wrong form scopes the gate to zero rows and every rule reports PASS over an empty
subject — green, and meaningless.

If it fails, the batch is not done. Fix the rows, re-emit, re-run. Do not
baseline the failure away: `governance/research-contract-baseline.json` ratchets
DOWN only, and raising a count there forgives fresh violations invisibly.

When it passes, confirm the corpus posture has not regressed:

```
python3 scripts/audit/research_batch_dod.py --all
```

Then commit the scratchpad and the agent transcripts (`scripts/preserve_transcripts.py`)
— a read-only subagent writes nothing at all, so its entire workings live in
ephemeral container storage until they are copied out.

## COVERAGE (read it; it does not fail)

A batch can read a document whose provisions are for blind, Deaf, cognitive and fatigue-limited people and still
write only mobility figures, because those are the quantities the catalogue holds. Print what the catalogue can
and cannot speak about, read-only, against the database the batch used (`GUIDEBOOK_DB_PATH`, else
`data/guidebook.db`). Add `--all` to read (3) over every source, not only this batch's. **Quote the three reads in the
pull request body: the owner reads coverage there.** Every count is printed beside its query; none is typed here.
Printed, not failed: zero is the honest state of most of the catalogue, and a check that is red by construction
teaches its reader to ignore it (CLAUDE.md rule 6).

```
python3 -I - $ARGUMENTS <<'PY'
import os, re, sys, sqlite3
db = os.environ.get("GUIDEBOOK_DB_PATH") or "data/guidebook.db"
c = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
if set(sys.argv[1:]) - {"--all"}: sys.exit(f"unknown argument(s) {sorted(set(sys.argv[1:]) - {'--all'})}: the only one is --all")
all_sources = "--all" in sys.argv
session = re.sub(r"\.md$", "", open("scratchpad/CURRENT").read().strip()) if os.path.exists("scratchpad/CURRENT") else ""
VS = "x.figure_role IN ('claim','derived')"
LENSES = (("identity_code", "SELECT identity_code FROM base_taxonomy_identity WHERE status='active'"),
          ("needs_code", "SELECT need_code FROM access_needs"), ("icf_code", "SELECT icf_code FROM base_icf"))
params = [r[0] for r in c.execute("SELECT parameter_id FROM base_parameters WHERE status='active' ORDER BY 1")]
print("(1) LENS BY PARAMETER: distinct live value-supplying figures per (lens code, active parameter)")
for col, reg in LENSES:
    q = (f"SELECT COUNT(DISTINCT x.extraction_id) FROM source_value_extractions x JOIN v_live_lens_links l "
         f"ON l.extraction_id = x.extraction_id WHERE {VS} AND x.parameter_id = ? AND l.{col} "
         + ("IN (WITH RECURSIVE f(c) AS (SELECT ? UNION SELECT i.identity_code FROM base_taxonomy_identity i JOIN f ON i.parent_code = f.c) SELECT c FROM f)"
            if col == "identity_code" else "= ?"))   # a parent's cell counts its descendants' figures (T-055)
    codes = [r[0] for r in c.execute(reg)]
    zero, cells = [], []
    for code in codes:
        n = [c.execute(q, (p, code)).fetchone()[0] for p in params]
        (zero if not any(n) else cells).append((code, [(p, k) for p, k in zip(params, n) if k]))
    print(f"  {col}: {len(codes)} codes x {len(params)} active parameters; query: {q}")
    print(f"    codes with ZERO figures against every parameter (a group the catalogue cannot speak about): {[z[0] for z in zero]}")
    for code, nz in cells: print(f"    {code}: {nz}")
print("(2) LENS BY FIGURE: value-supplying figures with a live link")
umbrella = {r[0] for r in c.execute("SELECT parent_code FROM base_taxonomy_identity WHERE parent_code IS NOT NULL")} | {"ALL"}
rows = c.execute(f"SELECT x.extraction_id, group_concat(l.identity_code), group_concat(l.icf_code), group_concat(l.needs_code) "
                 f"FROM source_value_extractions x JOIN v_live_lens_links l ON l.extraction_id = x.extraction_id "
                 f"WHERE {VS} GROUP BY x.extraction_id").fetchall()
ident_only = [r[0] for r in rows if r[1] and not (r[2] or r[3])]
umb_only = [r[0] for r in rows if r[1] and set(r[1].split(",")) <= umbrella and not (r[2] or r[3])]
print(f"  figures with a live link: {len(rows)}; identity links ONLY: {len(ident_only)}; filed only to ALL or a parent code: {len(umb_only)} {umb_only}")
print("(3) GROUP WORDS WITH NO PARAMETER: observations whose latest adjudication is DEFERRED, NOT-OURS or none")
q3 = ("SELECT o.ref_id, o.observation_id, o.surface_form, o.locator, COALESCE(a.outcome, 'none') FROM observed_terms o "
      "LEFT JOIN term_adjudications a ON a.adjudication_id = (SELECT MAX(adjudication_id) FROM term_adjudications WHERE observation_id = o.observation_id) "
      "WHERE COALESCE(a.outcome, 'none') IN ('DEFERRED', 'NOT-OURS', 'none')")
mine = set() if all_sources else {r[0] for r in c.execute("SELECT ref_id FROM evidence_sources WHERE created_by_session = ? UNION SELECT ref_id FROM source_scans WHERE created_by_session = ?", (session, session))}
print(f"  query: {q3}  (sources: {'all' if all_sources else f'this batch, session {session!r}: {len(mine)}'})")
by = {}
for ref, oid, form, loc, out in c.execute(q3 + " ORDER BY o.ref_id, o.observation_id"):
    if all_sources or ref in mine: by.setdefault(ref, []).append((oid, form, loc, out))
for ref, obs in by.items():
    print(f"    {ref}: {len(obs)} observation(s)")
    for oid, form, loc, out in obs: print(f"      #{oid} [{out}] {form!r} @ {loc}")
PY
```

Then gate the diff once, when the batch is ready to open a PR: `scripts/preflight.sh`
(CLAUDE.md §1) — not `run_checks.py --all`.
