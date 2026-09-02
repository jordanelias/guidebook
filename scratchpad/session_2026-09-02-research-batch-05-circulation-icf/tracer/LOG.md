> **Defect STATUS has one home: `../DEFECT-REGISTER.md`.** This log is the session
> narrative and holds the evidence for each finding; the register holds whether it is
> open. Where they differ the register is right. D05-017 was WITHDRAWN after this log
> was written: it rests on commit `645a6b9`, which was amended to `2718457` before any
> push and is not an ancestor of HEAD, so the over-claim never entered pushed history.

# TRACER LOG — session_2026-09-02-research-batch-05-circulation-icf

Author: tracer (Sonnet 5). Records only; does not adjudicate research quality (an antagonist does
that separately) and proposes no fixes beyond naming what is broken. All DB reads are
`mode=ro` against a copy of `/tmp/claude-0/-home-user-guidebook/6a6f63cd-b4d8-5e57-9230-c5afb931a48a/scratchpad/batch05.db`
(the batch-05 scratch) and, for baseline comparison, `data/guidebook.db` (canonical, untouched:
sha256 `1dc3369022bcacb4502ea8c8221c3c2fd074e9f2790a9fe8b10a647bf5181eb1` before and after this
audit). Snapshot time for all scratch-DB figures below: **2026-09-02 21:39 UTC**. The batch was
still live at that instant (scratch DB mtime 21:35:56, size still changing across this audit), so
this log is a snapshot, not a close-out record.

This continues the defect register already committed for this session
(`scratchpad/session_2026-09-02-research-batch-05-circulation-icf/DEFECT-REGISTER.md`, D05-001
through D05-007, written by an earlier tracer pass at ~20:45 and reviewed here rather than
restated) and the ID convention set by
`scratchpad/session_2026-09-01-research-batch-04-accessible-circulation/DEFECT-REGISTER.md`
(D04-001..032). New IDs below continue as **D05-008** onward.

---

## 1. PROVENANCE

### 1.1 Git commits, in order (branch `claude/accessible-circulation-research-b0flk1`)

Today's history before the batch-05 frame is batch-04 close-out work (PR #126 merge at
`fe616a4` 14:31 local / 20:31 UTC, then `80970d8`→`a90a36e`→`71a0f4a`→`011ff77`→`6a75e30`→
`c8e0a13`→`969e00c`→`21496e3`, ending 20:02 UTC) — out of this tracer's scope except where it
supplies context (D04-032 below). Batch-05 proper begins at `82dbf9a`:

| Commit | UTC time (author) | Msg timestamp | Summary |
|---|---|---|---|
| `82dbf9a` | 20:34:04 | 20:34 | `FRAME.md` authored, ICF-first, no item codes (D-0187) |
| `0243475` | 20:40:07 | 20:40 | Batch-05 retrieval-log directory + manifest first appear |
| `5d0b4ac` | 20:45:34 | 20:45 | Earlier tracer pass: `AUDIT-LOG.md` + `DEFECT-REGISTER.md`, D05-001..007 |
| `39e5b9b` | 21:04:07 | 21:04 | `retrieval_log.fetch()` bytes/`-L` fix (root cause of D04-032) |
| `fd26b18` | 21:21:11 | 21:21 | `--verify-authors` given-name/title/index fix + `db.py correct-source` writer |
| `645a6b9` | 21:30:57 | 21:33 | Euan's Guide re-retrieval, `REF-00978` admitted + `db.py amend-search` writer |

Interspersed among these are **~17** auto-generated `governance: session command log [...]`
commits (rule §0.6 compliance — commit the scratchpad at natural breaks), each appending to
`scratchpad/session_2026-09-01-research-batch-04-accessible-circulation/commands.jsonl` — **not**
to a batch-05-named file. That misfiling is itself D05-004 (below); it is still live as of this
audit (`git status --short` at the time of writing shows only that one file modified, uncommitted,
and this tracer's own commands are landing in it too).

**HEAD (`645a6b9`) is not the last activity.** After that commit landed, further `db.py` writes
ran against the scratch DB (never committed to git, because the scratch DB is outside the tree by
design until migration) — see §1.4 and D05-017.

### 1.2 Rows written to the batch-05 scratch, by table (delta against the canonical baseline,
independently re-queried against both DBs, not taken from any brief)

Canonical `data/guidebook.db` at this same moment: `evidence_sources`=0, `search_executions`=28,
`search_candidates`=60, `citation_mining`=10, `evidence_population_match`=0,
`evidence_source_authors`=0, `search_admissions`=0, `source_slug_links`=0 — i.e. the scratch write
path is working as documented and nothing has leaked into canonical mid-batch.

| Table | Canonical | Scratch (snapshot) | Delta |
|---|---|---|---|
| `evidence_sources` | 0 | 9 | +9 (`REF-00784` upgraded from a pre-existing `REFERENCE-ONLY` stash row; `REF-00971`–`REF-00978` newly inserted) |
| `evidence_source_authors` | 0 | 38 | +38 |
| `evidence_population_match` | 0 | 13 | +13 |
| `search_admissions` | 0 | 9 | +9 |
| `source_slug_links` | 0 | 9 | +9 (local ref `ACG-01`..`ACG-09`, all on slug `accessible-circulation-geometry`) |
| `search_executions` | 28 | 43 | +15 (`exec_id` 29–43) |
| `search_candidates` | 60 | 75 | +15 |
| `citation_mining` | 10 | 13 | +3 (backward mining on `ACG-04`/`REF-00973`, `ACG-05`/`REF-00974`, `ACG-08`/`REF-00977`) |
| `gaps` | 5 | 5 | 0 — no new gap row written by this batch |
| substrate (`slugs`, `axes`, `access_needs`, `populations`, `terms`, `term_aliases`, `research_code_leads`, `source_locators`) | unchanged | unchanged | 0 — batch-05 wrote no substrate rows |

Sum over the 15 new `search_executions` rows: `results_found`=303, `results_screened`=153,
`results_admitted`=9 (`SUM()` query, not hand-counted).

`evidence_population_match` breaks down by `target_population`: ALL=1, MOB=9, PAIN=1, SCI=2
(=13, matches the table total).

### 1.3 Retrieval — payloads and bytes (from `retrieval-log/session_2026-09-02-research-batch-05-circulation-icf/manifest.jsonl`, parsed, not hand-counted)

- **39 manifest lines, 39 distinct artefact files**, `exit`=0 on every line.
- **Total bytes received: 4,378,736** (`sum(bytes)` over all lines, including the one 0-byte line
  below).
- File-type breakdown by artefact extension: **28 `.json`, 6 `.html`, 2 `.txt`, 2 `.xml`, 1
  `.pdf`.**
- **One 0-byte artefact**: `e3b0c44298fc1c14.txt`, `sha256` = the sha256 of the empty string,
  `url=https://ndownloader.figshare.com/files/41261199`, logged *before* the `-L` fix — kept, not
  deleted, as the manifest's own evidence of the pre-fix redirect-stub bug.
- **The one `.pdf` line** — `f07d3924aaec6708.pdf`, 3,344,268 bytes, the Euan's Guide Access
  Survey report — is confirmed the first PDF this repository's `fetch()` has ever produced:
  every earlier PDF in any `retrieval-log/` directory (`CAOT_Home_Assessment_and_Modifications
  _2024.pdf`, `RCOT_Adaptations_Without_Delay_2019.pdf`, `RNIB_Seeing_Streets_Differently_2021
  .pdf`, `UCL_Childs_2009_kerb_heights.pdf`, `geoerg2019.pdf`, all under batch-04's directory)
  carries a **descriptive filename**, not a sha256-prefixed one — the naming `fetch()` never
  produces — confirming those were saved by hand, not logged by the tool.
- Two further PDFs used for full-text reading in this batch — `agonist/goodwin2022.pdf` (backing
  `REF-00975`) and `agonist/marchiori2023.pdf` (backing `REF-00973`) — were fetched by raw `curl`
  directly to the `agonist/` scratch directory, **not** through `fetch()`, and their sha256 values
  (`ec6f233f…fb34`, `61ee4e7a…327eb`) appear only in `agonist/BRIEF.md` prose. Grepped the
  manifest for both hashes: **zero matches**. See D05-018.

### 1.4 Corrections applied to the scratch this session (via `scripts/db.py`, re-verified against
the current DB state, not taken from commit prose)

- `correct-source --ref-id REF-00976 --field pub_title` and a given-name correction: stored title
  now reads `"ACUTUAL FEATURES OF ORIENTATION TO LIFE TIME HOMES FROM VIEWPOINTS OF WHEEL CHAIR
  MOVEMENTS POSSIBILITY"` (typo preserved verbatim, per the source); author 5 now reads `HASEGAWA,
  Naoji` (was `Toshiyuki`) — confirmed by direct query of `evidence_source_authors`.
- `correct-source --ref-id REF-00973 --field pub_title`: stored title now reads `"Quantification
  of the Risk of Musculoskeletal Disorders of the Upper Limb Using Fuzzy Logic: A Study of Manual
  Wheelchair Propulsion"` — confirmed by direct query.
- Volume/issue/article_number fields: counted non-null values across all 9 `evidence_sources`
  rows directly — **16** (`REF-00784`:2, `REF-00971`:2, `972`:2, `973`:2, `974`:2, `975`:2,
  `976`:2, `977`:2, `978`:0) — matches the commit's claim of "sixteen NULL … fields" corrected,
  independently reproduced rather than taken on trust.
- `amend-search --exec-id 34` and a second, separate `amend-search --exec-id 43` (see §1.5): both
  confirmed present in `search_executions.findings_note` via direct query, using the `"|| CORRECTED
  2026-09-02:"` marker the commit describes; the pre-correction text is unmodified ahead of the
  marker in both rows (append-only, as designed).
- `research_batch_dod.py --session session_2026-09-02-research-batch-05-circulation-icf` run
  independently by this tracer against the scratch (env-var pointed, canonical file never opened
  other than `mode=ro`): **COMPLIANT — all 17 rules PASS**, reproducing the commit's claim exactly.
- `retrieval_log.py --verify-authors --session session_2026-09-02-research-batch-05-circulation-icf`
  run independently: **`EXAMINED: 8`, `CLEAN`** — reproducing "EXAMINED goes 5 → 8" and "CLEAN on 8
  examined" exactly.

### 1.5 Activity after `645a6b9` (HEAD), not captured in any commit

The scratch DB continued changing after the last commit. Commands in the (misfiled) command log
timestamped 21:34–21:36 UTC show, and direct query of the scratch confirms:

- A **second** `amend-search` correction, applied to **both** `exec_id 34` and `exec_id 43`,
  appending `"R15 applied to my own writing: the ranking as first recorded OVER-CLAIMED…"` — see
  D05-017.
- `add-population-match --ref-id REF-00978 --target-population ALL` and `--target-population MOB`
  (both `match_grade=PARTIAL`, `created_at 21:34`).
- `resolve-candidate --candidate-id 73 --disposition ADMITTED --admitted-ref-id REF-00978`
  (`search_candidates.notes` for candidate 73 already carries the corrected, non-over-claiming
  ranking text — this write ran *after* the R15 correction above, so it is internally consistent
  with it even though the commit and the first correction layer are not; see §5).

None of this is in `git status` as a pending change, because it lives entirely in the
out-of-tree scratch DB, which is the documented write path pending migration — not itself a
defect. It is recorded here because a reader of `git log` alone would not see it.

---

## 2. DEFECTS FOUND AND FIXED THIS SESSION

Each verified against the actual diff and/or current DB state, not taken from the commit message
alone.

### D05-008 — `retrieval_log.fetch()` could not log a PDF; this is D04-032's undiagnosed root cause
- **Fixed in:** `39e5b9b`.
- **What was broken:** `fetch()` ran `subprocess.run(["curl","-sS",...,url], capture_output=True,
  text=True)`. `text=True` forces `curl`'s stdout to be UTF-8-decoded before `fetch()` sees it; on
  a genuinely binary body this raises `UnicodeDecodeError` **before the artefact is written**.
  Reproduced against a 10,256-byte fixture, quoted in the commit: `'utf-8' codec can't decode byte
  0x80 in position 137`. Separately, no `-L` was passed, so a redirecting URL (a DOI) stored the
  302 stub rather than the target — the 0-byte `e3b0c44298fc1c14.txt` figshare line (§1.3) is that
  bug's own artefact, preserved in the manifest as evidence.
- **Fix:** capture bytes (`text=False`, drop `capture_output` text mode), add `-L`, sniff format by
  magic number on bytes (`_extension_for` rewritten to accept `bytes`, PDF/`zip`/OLE2/BOM
  detection added), hash and `write_bytes()` what actually arrived, decode tolerantly
  (`errors="replace"`) only to attempt a JSON parse, never to store.
- **Verified:** the fixed function's own output — `f07d3924aaec6708.pdf`, 3,344,268 bytes — is now
  in the manifest (§1.3); confirmed first PDF the tool itself has ever logged, by filename
  convention as above.

### D05-009 — `--verify-authors` compared family names only; a given-name substitution passed as CLEAN
- **Fixed in:** `fd26b18`.
- **What was broken:** `verify_authors()` built `real`/`stored` author lists from family name
  alone. `REF-00976` stored co-author given name `Toshiyuki` where every logged payload said
  `Naoji` (same family name, `HASEGAWA`) and the checker reported CLEAN — five matching surnames,
  nothing checked further.
- **Fix:** `_given_conflict()` + `_given_tokens()` added — compares given names as name-part tokens
  under an initial-prefix rule (so `"J."`/`"Jonathan"`, `"Dirkjan (H. E. J.)"`/`"Dirkjan H. E. J."`,
  `"Wiebe H.K."`/`"Wiebe H. K."` are not flagged) while `"Naoji"`/`"Toshiyuki"` is. `_author_conflict()`
  now checks family-name order first, then given-name conflict.
- **Verified:** `evidence_source_authors` for `REF-00976` position 5 now reads `Naoji` (§1.4);
  `--verify-authors` independently re-run, CLEAN.

### D05-010 — `--verify-authors` indexed only Crossref single-work payloads; three sources read as unverifiable while their payload sat on disk
- **Fixed in:** `fd26b18`.
- **What was broken:** the by-DOI index built from `msg.get("message")` with `msg["DOI"]` present
  — the shape Crossref returns for a single work. Unpaywall files the DOI at top level with authors
  under `z_authors`; a Crossref *search* result files works under `message.items`. Three of eight
  sources this batch had payloads logged only in those shapes and were reported "NO LOGGED
  RETRIEVAL — not verifiable offline."
- **Fix:** `_index_by_doi()` rewritten to read all three envelope shapes, ranked (Crossref
  single-work > Crossref search item > Unpaywall) so a richer record is never displaced by a
  thinner one of the same DOI; `_from_unpaywall()` reshapes an Unpaywall record into the compared
  keys, carrying across only fields Unpaywall actually states.
- **Verified:** `EXAMINED` count went from 5 to 8 on the *same* retrieval log (independently
  reproduced, §1.4) — a strictly larger subject with no change to which payloads exist.

### D05-011 — a curly apostrophe produced a false FAIL on `REF-00975`
- **Fixed in:** `fd26b18`.
- **What was broken:** `_norm()` folded accents (NFKD + strip combining marks) but not typographic
  punctuation. Author 6 on `REF-00975` is stored as `D'Cruz` (straight apostrophe, confirmed by
  direct query, §1.4); a payload rendering it with a curly `’` printed a FAIL purely on the glyph
  difference — the docstring states this was, before today, "the whole of the single FAIL this
  checker printed."
- **Fix:** `_PUNCT_FOLD` translation table added to `_norm()`, folding curly/straight quotes,
  various dash forms, and backtick/acute-as-apostrophe variants to one canonical form each.
- **Verified:** `REF-00975` author 6 confirmed stored as `D'Cruz`; `--verify-authors` independently
  re-run, CLEAN (no FAIL of any kind on the current examined set).

### D05-012 — three fabricated bibliographic fields filed in the batch (two titles, one given name)
- **Fixed in:** `fd26b18` (via the new `db.py correct-source` writer, §1.4).
- **What was broken:** `REF-00976` stored a title no payload asserts (the commit does not quote the
  original wrong string) and the `HASEGAWA Toshiyuki` given-name substitution (D05-009).
  `REF-00973` stored a title "bent toward the slug it was admitted for" — the commit quotes the
  wrong stored form as `"…During Manual Wheelchair Propulsion on Different Slopes"` against the
  paper's actual subtitle `"A Study of Manual Wheelchair Propulsion."`
- **Fix:** all three fields rewritten from the logged payload via `correct-source` (D05-014), never
  retyped from memory.
- **Verified:** current stored titles and the `Naoji` given name confirmed by direct query (§1.4);
  no unresolved bibliographic mismatch remains — `--verify-authors` CLEAN.

### D05-013 — the batch's one disability-led source was screened out on a false 404-page characterisation
- **Fixed in:** `645a6b9` (plus an uncommitted follow-up correction, §1.5 / D05-017).
- **What was broken:** `exec 34`'s original `findings_note` gave two reasons nothing was admitted
  from the Euan's Guide Access Survey: the report URL "returns HTML rather than the PDF," and its
  content is "predominantly information provision, toilets and staff attitude rather than
  circulation geometry." The logged payload for that fetch, `72c0fcb12f42614c.html` (15,580 B), is
  a "Page not found" page containing no occurrence of "survey," "respondent," "toilet," or "staff"
  — independently confirmed the description is not merely imprecise but unsupported by any
  retrieved byte.
- **Fix:** five further fetches under a new re-retrieval, all logged (§1.3), reaching the live
  report (`f07d3924aaec6708.pdf`, 29 pp.) via the homepage → `/accesssurvey` → S3. Admitted as
  `REF-00978` / `ACG-09`, `evidence_type=co1`, `tier=1`, `jurisdiction=GB` — confirmed by direct
  query (§1.2). `db.py amend-search` (D05-014) used to append the correction to `exec 34`'s
  `findings_note` without altering the original text (R8 append-only).
- **Verified:** `evidence_sources` row for `REF-00978` confirmed present with the stated fields;
  `search_admissions` and `source_slug_links` rows confirmed (§1.2). The specific numeric claim in
  this same commit ("most-cited barrier … ahead of entrance access") was itself later found to be
  an over-claim by the same session and re-corrected outside git — see D05-017, which this entry
  does not resolve.

### D05-014 — `db.py` had no writer to correct a bibliographic field, and none to correct a logged search note
- **Fixed in:** `fd26b18` (`correct-source`) and `645a6b9` (`amend-search`).
- **What was broken:** no CLI path existed to fix a wrong bibliographic field once written, nor to
  annotate a wrong `search_executions.findings_note` (append-only per R8, so no path could ever
  have allowed rewriting it outright without breaking that rule).
- **Fix — `correct-source`:** takes `--ref-id` and repeatable `--field` naming *which* field to
  correct; there is no flag for the value — the value is always read from the logged payload for
  that ref's DOI (`_payload_for()`). Refuses on: unknown ref, no DOI, no retrieval log for the
  named session, no payload logged for that DOI, a payload silent on the requested field. The
  correctable-field set (`_CORRECTABLE`) is defined as exactly the fields `--verify-authors` can
  prove, by design, so this writer cannot become a second way to assert an unverifiable value.
  Confirmed present in `scripts/db.py` and exercised (§1.4).
- **Fix — `amend-search`:** takes `--exec-id` and `--append-note`; appends
  `"|| CORRECTED <date>: <note>"` to the existing `findings_note`, never rewriting the prior text.
  Refuses on an empty note or an unknown `exec_id`. Confirmed present and exercised on `exec 34`
  (twice, across two different corrections — §1.5) and `exec 43` (once).
- **Also swept:** a docstring in `retrieval_log.py` pointing at
  `scripts/audit/author_fidelity_audit.py` — confirmed that file no longer exists on disk, and the
  one remaining repo reference to its name is the historical "since-retired" mention in the same
  docstring, not a live pointer.

---

## 3. DEFECTS FOUND AND NOT FIXED

Carried forward from the earlier tracer pass (`DEFECT-REGISTER.md`, D05-001..007), re-checked
against current state, plus new items this final pass found.

- **D05-001** (`slugs.serves_axes` populated on 1/106, not this slug) — still OPEN, correctly not
  blocking per DR-2026-08-24 §2.4. No change.
- **D05-002** (no term↔slug link; R11 `terms_used` not pointer-derivable) — still OPEN, same
  reasoning. No change.
- **D05-004** (command-log hook misfiling this session's Bash commands into batch-04's
  `scratchpad/session_2026-09-01-research-batch-04-accessible-circulation/commands.jsonl`) — **still
  live at the moment of writing this log.** `git status --short` shows only that file modified;
  this tracer's own diagnostic commands from this very pass are appended to it, not to any
  batch-05-named file. Root cause per the earlier register entry:
  `.claude/hooks/record-command.py`'s `open_session()` anchors on the harness session id
  (`6a6f63cd-b4d8-5e57-9230-c5afb931a48a`), shared across every role in this multi-agent batch
  (orchestrator, agonist, antagonist, tracer), and does not re-derive when a new *project* session
  starts inside the same harness container. Not fixed this session; resolution requires either
  seeding a batch-05 `commands.jsonl` line carrying this session id, or a post-hoc split at close —
  neither attempted here, per the earlier register's own statement that this is an orchestrator
  action.
- **D05-005** (no contemporaneous manifest existed yet at session start) — **final observation
  made, not previously recorded**: the watch condition has resolved cleanly. `manifest.jsonl` for
  this session now has 39 lines, **zero** marked `"reconstructed": true` (checked directly), unlike
  batch-04's manifest (all 21 lines `"reconstructed": true`, restored after the fact). This
  session's retrieval was logged contemporaneously via `fetch()` throughout, once D05-008 was
  fixed mid-batch.
- **D05-006** (`sessions/LATEST-RESEARCH` names batch-02; batch-03 is the DB-newest research
  session) — **still stale, re-confirmed at time of writing**: `cat sessions/LATEST-RESEARCH` still
  returns `session_2026-08-22-research-batch-02-room-acoustic-performance.md`.
  `SELECT DISTINCT session FROM search_executions` on the *canonical* DB still returns exactly
  batch-01/02/03 (batch-05's writes are in the scratch only, not yet migrated). Deferred to
  session close by design (moving it mid-batch would re-scope the gate under the very batch it
  should audit) — not fixed, and will need action at close, now naming batch-05 rather than
  batch-03 once this batch's evidence is migrated.
- **D05-015 (new)** — `AUDIT-LOG.md` (committed in `5d0b4ac`) cross-references "`DEFECT-REGISTER
  D05-000`" twice (lines 9 and 25) for what is, in the committed `DEFECT-REGISTER.md`, entry
  **D05-007** ("Tracer's own verification method…"). No `D05-000` entry exists in the register.
  Dangling/mismatched ID between the session's own two audit artefacts, produced in the same
  commit.
- **D05-016 (new)** — the Euan's Guide re-retrieval fetch count is stated three different ways for
  the same event and none of them is hand-verifiable without the manifest: the `645a6b9` commit
  body says *"Five fetches, all logged"*; `exec 43`'s own `findings_note` (written the same
  session) says *"Four further fetches were logged"*; the manifest diff for that commit adds
  **six** new lines (`5f535ff1…html`, `145a47aa…html`, `2829878…html`, `2c51ce39…html`,
  `aaae2672…html`, `f07d3924…pdf` — confirmed by `git show --stat` and by direct count of the
  diff's added manifest lines). None of the three prose counts matches the derived one — CLAUDE.md
  §2(b) ("no hand-written counts in derived documents… generate them from the DB") applies to a
  commit message and a DB note exactly as it would to a rendered report, and neither the immutable
  commit body nor the DB note has been corrected to the derived figure.
- **D05-017 (new)** — the git-committed record of the Euan's Guide finding is now known, by the
  same session's own later work, to overstate its central claim, and nothing points a reader from
  the committed text to the correction. Detailed in §5; ID retained here for the open-items list.
- **D05-018 (new)** — the two full-text PDFs actually read for this batch's content claims
  (`goodwin2022.pdf` behind `REF-00975`, `marchiori2023.pdf` behind `REF-00973`) were fetched by
  raw `curl` to `agonist/`, bypassing `fetch()`, before D05-008 was fixed — and were never
  re-fetched through the fixed `fetch()` afterward. Their sha256 values live only in
  `agonist/BRIEF.md` prose (§1.3), not in `retrieval-log/…/manifest.jsonl`. `--verify-authors`
  passing CLEAN does not cover this gap: it examines the separately-logged Crossref bibliographic
  JSON for these DOIs, not the full-text PDFs used for the batch's page-and-table-level claims (the
  quantified findings in §6 of `agonist/BRIEF.md` that carry `[FULL]` tags). The tool that was
  fixed specifically to close this class of gap (D05-008) was not applied retroactively to the two
  PDFs the fix was motivated by.

Also checked and found **not** stale or contradictory as of this pass: `sessions/LATEST` (points at
`session_2026-09-02-owed-repairs.md`, the correct prior closed session; distinct pointer from
`LATEST-RESEARCH`, per CLAUDE.md §7 trap 2). No session record yet exists for batch-05
(`sessions/session_2026-09-02-research-batch-05-circulation-icf.md` absent) — expected, the batch
has not closed.

`gaps` table (5 rows, all inherited from batch-01/02, none created by or attributed to batch-05):
unchanged by this session, listed for completeness — `GAP-B01-001`..`004`, `GAP-B02-001`, all
`status=OPEN`.

---

## 4. GAPS AND FAILURES IN THE WORK ITSELF

Quoted from `search_executions.findings_note` / `deferred_reason` directly, not summarised away.

**The one deliberate non-search** (`exec 42`, `query_text` = `[NOT SEARCHED] vertical circulation
as a sub-construct: passenger lifts, platform lifts, evacuation lifts`):
> "DELIBERATELY NOT SEARCHED, and not for want of budget. Vertical circulation is the one part of
> this slug whose determinative literature is standards-and-conformity (EN 81-70, EN 81-41, ISO
> 21542, ASME A18.1) rather than measured human demand, and the 2026-08-12 REFERENCE-ONLY ruling
> means those documents may be NAMED as leads but not mined for values. An evidence search here
> would have produced a list of standards that cannot be quoted plus a thin scatter of entrapment
> case reports — high cost, near-zero admissible yield, and a standing risk of smuggling a code
> value into a research row. NO CLAIM IS MADE ABOUT LIFT DIMENSIONS."

**Query-shape failures (R14), engine returned the wrong index for the question asked:**
- `exec 31` (blind/deafblind wayfinding, PubMed): "PubMed `query_translation` expanded blind to
  `\"blinded\"[All Fields] OR \"blinding\"[All Fields]`" — RCT masking — "returning Ethiopian SRH
  services and a vaccination RCT protocol. 1 of 10 on-topic. Blind-navigation work also lives in
  HCI and architecture venues PubMed does not index."
- `exec 40` (injury/entrapment AND-chain, PubMed): "MeSH expanded lift to `\"lifting\"[MeSH]`, fall
  to Accidental Falls and trauma to Wounds and Injuries, returning dry-beriberi physiotherapy, a
  brain-computer-interface door opener and spinal-cord-injury fracture epidemiology. 1 of 7
  on-topic. The R7 harm class is not reachable from PubMed by AND-chaining these concepts." — the
  batch's own harm-search (H-8 in `agonist/BRIEF.md`) states plainly: "The Deaf/blind entryphone
  question in particular returned nothing at all and is completely unevidenced in this batch."
- `exec 35` (RCOT falls-prevention guideline): "ZERO-YIELD for the guideline document, kept. R14
  WRONG INDEX: RCOT practice guidelines are member-gated, so the web tier returns commentary about
  them and never their recommendation text."

**Genuine absences (well-formed query, right index, confirmed nothing there):**
- `exec 33` (OT professional-body guidelines by name): "ZERO-YIELD, kept. The search engine itself
  concluded the results do not address detailed guidelines from RCOT, WFOT or AOTA, nor
  dimensional specifications."
- `exec 36` (OT Practice Guidelines by title-field): "R14 GENUINE ABSENCE and it is a finding
  rather than a search artefact. All five retrieved and read at abstract level across three
  professional bodies and two independent search paths: the OT professional-body guideline
  literature carries no environmental-parameter content. The Co-2 negative is structural." —
  cross-checked against `agonist/BRIEF.md` §2.1, which names the five PMIDs read.
- `exec 32` (DPO reports on circulation barriers): "R14 GENUINE ABSENCE OF THIS GENRE, not of the
  topic. Disabled people organisation output in this territory addresses supply and policy —
  waiting lists, wheelchair-home targets, housing-market assessment data gaps — not the demand a
  corridor places on a body. The two admissions attributed here are ACADEMIC sources the engine
  surfaced in answer to a DPO-targeted query; the DPO genre itself yielded nothing admissible."

**Index-scope caveats, logged as such rather than as absence:**
- `exec 30` (Scholar Gateway): "INDEX CAVEAT recorded by the retrieving agent: Scholar Gateway
  returned only Wiley-published items. That is a publisher-scoped index, not a field index, so its
  silence is not evidence of absence."
- `exec 39` (German-language query, Consensus): "HONESTY NOTE from the retrieving agent: Consensus
  is a semantically English-centric index, so a German query returned English-language results.
  The QUERY was non-English; the INDEX was not."

**Coverage the batch did not reach, per `agonist/BRIEF.md` §9.3** ("Absent from my search only —
do NOT read these as absence of evidence"): everything about vertical circulation (by design, see
`exec 42` above); automatic-door entrapment, internal-threshold injury and Deaf/blind entryphone
inaccessibility (wrong instrument, per `exec 40`); non-Anglophone literature other than one
Japanese-language pass (German/DIMDI/LIVIVO/TIB, Nordic/SwePub, Francophone/HAL/Cairn, Chinese/CNKI
all untouched); the interior of five of the batch's eight admissions, which are paywalled and read
at abstract level only (`A1`, `A2`, `A3`, `A5`, `A8` — every quantified claim from them is tagged
`[ABS]` in the brief's §6, not `[FULL]`); 11 of the 17 ICF axes in the frame, meaningfully probed
"roughly six" (`AX-WHM`, `AX-AMB`, `AX-BAL`, `AX-PAI`, `AX-STA`, weakly `AX-COG-O`) — thermal load,
sensory load and toileting-proximity as circulation constraints are named explicitly as untested.

**A one-record national-index seam, stated as a coverage measurement rather than a finding about
content** (`exec 41`, J-STAGE): "THE R5 FINDING OF THE BATCH. 49 Japanese academic papers on
wheelchair x corridor x width in one national index; English-language engines surfaced one of
them." — `agonist/BRIEF.md` §9.4 draws the further, hedged implication that a 2003 Japanese paper
(`C-2`, not read) may predate the 2019 English-language paper batch-04 called its own highest-value
staged item, and states plainly: "I have not read it and I make no claim about its content."

**Tooling that refused, encountered live:**
- `db.py correct-source` refusing on a field outside the provable set (`--field journal…`,
  exercised deliberately at 21:20:12 per the command log, before the writer was used for real —
  five refusal paths named in the commit and confirmed exercised: unknown ref, no DOI, no
  retrieval log, no payload for the DOI, payload silent on the field).
- `T&F` (Taylor & Francis) returned HTTP 403 on the Bragança systematic-review candidate (`C-3`),
  leaving its risk-of-bias status (the fact that decides T2 vs T3 grading) unconfirmed and the
  source staged rather than admitted.

---

## 5. CONFLICTS AND CONTRADICTIONS

- **Resolved by design, not a live conflict:** `exec 34`'s `findings_note` carries, by the design
  of the new `amend-search` writer (D05-014), an appended correction that directly contradicts its
  own original text — the original claims the source was correctly screened out; the appended text
  says both original reasons were false. This is R8 append-only working as intended (never rewrite,
  always append with a dated marker) and is recorded here as resolved-by-design, not as an open
  contradiction.

- **`D05-006` — document vs. DB:** `sessions/LATEST-RESEARCH` states batch-02 as the subject of the
  blocking citation-mining gate; the canonical DB's own `search_executions`/`citation_mining`
  tables show batch-03 as the newest research session with rows in either. Currently produces an
  identical (vacuous) gate result either way because `evidence_sources` is 0 in canonical, so the
  conflict is latent rather than live — see full detail already on record in
  `DEFECT-REGISTER.md` D05-006.

- **`D04-032` register text vs. current code state:** `scratchpad/session_2026-09-01-research
  -batch-04-accessible-circulation/DEFECT-REGISTER.md`'s D04-032 entry (last touched `a90a36e`,
  18:24 UTC today, several hours before `39e5b9b`) still reads `Status: OPEN` with `Resolution
  owed: Run retrieval_log.py --backfill --session before any re-admission of this material.` It
  makes no mention of a root cause in `fetch()` itself, because at the time it was written the root
  cause had not yet been diagnosed — `39e5b9b`'s own commit message states this explicitly ("THIS
  IS WHY D04-032 HAPPENED… That treated the symptom: I never asked why they were unlogged. This is
  the answer"). The batch-04 register was not updated after `39e5b9b` landed; a reader of that file
  alone would not learn that the underlying tool defect has since been fixed, only that a
  `--backfill` workaround was identified for the symptom.

- **`D05-016`/`D05-017` — a commit's own prose vs. the same session's later self-correction:** The
  `645a6b9` commit body and the *first* correction layer on `exec 34`/`exec 43` both assert
  "Circulation geometry is the most-cited barrier class in the survey, ahead of the entrance access
  that accessibility practice most often addresses" (56% vs 41%). A **second**, uncommitted
  `amend-search` correction (§1.5) — applied after `645a6b9` and appended to the *same two* rows —
  states: "R15 applied to my own writing: the ranking as first recorded OVER-CLAIMED. Full option
  set of Q7 (p.13-14) is parking 64, could-not-get-around-the-venue 56 … So circulation geometry is
  NOT the most-cited barrier in the survey: parking at 64 percent outranks it. The defensible claim
  is that it is the most-cited IN-BUILDING barrier and second overall." This second correction:
  - is confirmed present in the current scratch DB (§1.5, quoted in full);
  - is **not** reflected in the `645a6b9` commit message, which is immutable once pushed and
    contains no forward pointer to it;
  - **is** already reflected correctly in `search_candidates.notes` for candidate 73 (resolved
    *after* the second correction, so internally consistent with it) and in the
    `evidence_population_match` mismatch notes for `REF-00978` (which describe the 56% figure
    narrowly and do not repeat the "most-cited overall" claim).
  Net effect: the git-committed record of this batch's own signature finding currently overstates
  it, the DB record has since been corrected twice, and only the DB — not the commit history — will
  carry the accurate claim forward unless something else is done at close.

- **Three counts of one event (D05-016):** see §3 — "Five fetches" (commit body) / "Four further
  fetches" (DB note, same event) / six new manifest lines (directly counted). All three describe
  the same re-retrieval and disagree with each other and with the manifest.

- **`AUDIT-LOG.md` vs. `DEFECT-REGISTER.md` (D05-015):** the audit log's own cross-references to
  "D05-000" name an entry that does not exist under that ID in the register committed in the same
  commit; the matching content is D05-007.
