# Defect register — session_2026-09-01-research-batch-04-accessible-circulation
Role: TRACER. Every conflict, error, contradiction, tool failure, gate failure, refusal and
surprise, as a numbered resolvable object. Per CLAUDE.md commit `a deviation is an object, not a
string`.

---

### D04-001 — Runbook Step 0 expectation ("exactly ONE failure: R1") is stale against the live DoD gate
- **Class:** DOC-DRIFT
- **Severity:** P3 cosmetic/latent (does not block the batch — the orchestrator already observed and worked past the real gate output)
- **Observed:** pre-session, by orchestrator; recorded into this log at 2026-09-01 20:17 by tracer
- **What happened:** `research_batch_dod.py --session <this session>` pre-batch run returned exit 1 with exactly three failures: R1 (no Co-1/Co-2 pass), R9a and R9b (both `NOTHING IN SCOPE`). DR-2026-08-19 §12.1's Step 0 text predicts "exactly ONE failure: R1", written when the gate had 15 rules.
- **Where:** `decisions/DR-2026-08-19-research-restart-operative-instrument.md` §12.1 Step 0, vs. `scripts/research_batch_dod.py` (now 17 seeded rules per its own `--selftest` output — R9a/R9b were added later under the OD-5 stash-widening work).
- **Why it matters:** A session following the runbook literally would see two failures the instrument's own text did not predict and could misread them as a new problem rather than an expected consequence of R9a/R9b existing on an empty pre-batch session. Low risk here because the orchestrator already correctly attributed both to NOTHING-IN-SCOPE, but the instrument text itself is now wrong and will mislead the next session that trusts it without running the gate first.
- **Status:** OPEN
- **Resolution owed:** Update DR-2026-08-19 §12.1 Step 0's stated expectation from "exactly ONE failure: R1" to reflect the current 17-rule gate's actual pre-batch signature (R1 + R9a NOTHING-IN-SCOPE + R9b NOTHING-IN-SCOPE), or make the text self-updating (derive rule count from the registry rather than hardcoding it), consistent with CLAUDE.md §2(b)'s ban on hand-written counts in derived documents.

---

### D04-002 — GAP-B01-001: batch-1 admitted sources never read in full (inherited, not caused by this session)
- **Class:** DATA
- **Severity:** P2 blocks a claim
- **Observed:** 2026-08-19, by `session_2026-08-19-research-batch-01-room-acoustic-performance`; carried forward and reconfirmed by tracer 2026-09-01 20:19 via read-only query against the live `gaps` table
- **What happened:** `"All five batch-1 admissions had FABRICATED author lists on first write (12 of 19 author rows named non-authors), corrected only after adversarial review. A human must re-read each source and confirm that the CONTENT claims made of it are sound, not merely that its bibliography now matches Crossref. The metadata is machine-verified; the reading is not."` (verbatim, `gaps.description` for `GAP-B01-001`)
- **Where:** `gaps` table, `gap_id='GAP-B01-001'`, `category=AUDT`, `priority=P1`, `status=OPEN`, `section=room-acoustic-performance`.
- **Why it matters:** Not on a batch-04 slug and does not block this batch's work. Recorded here because it is live, open, uncontested prior-session context this TRACER inherited on read of the `gaps` table, and because it is the direct precedent for why batch 04's own citation and author-fidelity work must leave a verification artefact (CLAUDE.md §2(c), `scripts/research/retrieval_log.py --verify-authors`) rather than trust machine-populated fields.
- **Status:** OPEN (inherited — this session did not cause it and has no mandate to close it)
- **Resolution owed:** `falsification_condition` per the row: "Closed when a reader other than the authoring session has read all five sources and confirmed or corrected every claim recorded against them." Not batch-04's responsibility to close.

---

### D04-003 — GAP-B02-001: batch-2 admitted sources never read in full, two specific unverified figures named (inherited, not caused by this session)
- **Class:** DATA
- **Severity:** P2 blocks a claim
- **Observed:** 2026-08-22, by `session_2026-08-22-research-batch-02-room-acoustic-performance`; carried forward and reconfirmed by tracer 2026-09-01 20:19 via read-only query against the live `gaps` table
- **What happened:** `"Batch 2 admitted five sources on metadata alone. No full text was read... Bettarello REF-00561 is credited in this project's own reasoning document with a 0.4-0.7 s RT60 recommendation that NOBODY HERE HAS SEEN IN THE PAPER; the two Iglehart papers are credited with a 0.3 s threshold on the strength of abstracts; and Markussen REF-00970 is graded PARTIAL for DEM on an abstract that does not establish whether people with dementia were interviewed directly or whether staff spoke as proxies."` (verbatim, `gaps.description` for `GAP-B02-001`)
- **Where:** `gaps` table, `gap_id='GAP-B02-001'`, `category=AUDT`, `priority=P1`, `status=OPEN`, `section=room-acoustic-performance`.
- **Why it matters:** Same class of risk as D04-002 — unread admissions standing in for verified claims — but with named, quantified figures at stake (0.4–0.7 s RT60, 0.3 s threshold). Not a batch-04 slug. Relevant precedent for batch 04's own admissions: a source being metadata-VERIFIED must not be conflated with its content claims being confirmed.
- **Status:** OPEN (inherited — this session did not cause it and has no mandate to close it)
- **Resolution owed:** Per `falsification_condition`: "Closed when a reader has read all five sources in full and confirmed or corrected every claim recorded against them — and specifically when the 0.4-0.7 s and 0.3 s figures are either verified from the sources with a locator, or struck." Not batch-04's responsibility to close.

---

### D04-004 — Four recent governance commit messages carry `[YYYY-MM-DD HH:MM]` timestamps that do not match their actual git commit time, with growing drift
- **Class:** DOC-DRIFT
- **Severity:** P3 cosmetic/latent (all four commits predate this session's branch point; does not block batch 04)
- **Observed:** 2026-09-01 20:17, by tracer, via `git log --format='%H %ad %s' --date=iso-strict-local` compared against each commit's embedded `[...]` message timestamp
- **What happened:** Measured on the four commits immediately preceding merge `708948a`:
  | Commit | Message timestamp | Actual commit time (UTC) | Drift |
  |---|---|---|---|
  | `c74e149` "the 44 WHO domains, and the e-codes they do not carry" | `[2026-09-01 21:30]` | `2026-09-01T19:07:31+00:00` | +2h23m |
  | `9b8040c` "e150 is not a lens, and the reason is doctrinal" | `[2026-09-01 22:05]` | `2026-09-01T19:16:30+00:00` | +2h49m |
  | `5a44fba` "A-K should not exist yet, and my recommendation ran the wrong way" | `[2026-09-01 22:40]` | `2026-09-01T19:22:37+00:00` | +3h18m |
  | `277a2e2` "every taxonomical code, sorted for categorization" | `[2026-09-01 23:20]` | `2026-09-01T19:28:35+00:00` | +3h52m |

  The embedded timestamps are internally sequential and plausible-looking (21:30 → 22:05 → 22:40 → 23:20, each ~35–40 min apart) but do not correspond to `date -u` at the actual commit time — real commit-to-commit gaps were 6–9 minutes, not 35–40. The drift itself grows by roughly 30 minutes per commit, which is not consistent with a single fixed clock offset.
- **Where:** Commit messages at `c74e149`, `9b8040c`, `5a44fba`, `277a2e2` (all on `origin/main`, predating this session's branch point).
- **Why it matters:** CLAUDE.md rule 1 requires the commit-message timestamp to be `date -u '+%Y-%m-%d %H:%M'` — the actual UTC time of commit, not a planned or narrative time. If the embedded time is not literally read off the clock at commit time, the format's only enforced property (per CLAUDE.md, "The commit-message format check remains") — that it parses — is satisfied while the value itself is fiction, which is exactly the shape of failure mode (c) in CLAUDE.md §2 ("a gate that passes having examined nothing... never whether they were true"). It is not this session's defect to have caused, but it is live on `main` and worth surfacing since this TRACER's own log is bound by the identical rule and a reader auditing timestamp provenance across sessions should not assume message timestamps are reliable without cross-checking `git log --date`.
- **Status:** OPEN
- **Resolution owed:** Either explain the drift (e.g., confirm whether these four commits were drafted with a stale/offset local clock, or composed non-interactively and time-stamped at draft rather than commit time) or correct the record. No CI gate currently catches this — the commit-format check (per CLAUDE.md: "still `if: github.event_name == 'push'`") verifies the *shape* of the `[...]` token, not that it equals the commit's actual timestamp; closing this durably would mean adding that cross-check, which is itself a new-apparatus decision for the owner/orchestrator, not this tracer.

---

### D04-005 — `bpc_metadata` table has zero rows repo-wide, so the RETRACTED-PRE-REHAB state of all 4 batch-04 target slugs (and 64 others) is invisible to any DB-only check
- **Class:** DATA
- **Severity:** P2 blocks a claim
- **Observed:** 2026-09-01 20:22, by tracer, via `sqlite3.connect('file:data/guidebook.db?mode=ro', uri=True)` read-only query
- **What happened:** `SELECT COUNT(*) FROM bpc_metadata` = 0 and `SELECT COUNT(*) FROM bpc_metadata WHERE evidence_state='RETRACTED-PRE-REHAB'` = 0 — the table is completely empty. Yet:
  - All four batch-04 target slugs' `bpc_path` files (`references/bpc/entrances-and-circulation/{accessible-circulation-geometry,stair-ramp-threshold-biomechanics-accessibility,threshold-door-hardware,threshold-and-level-access}.md`) each carry the header line `**SYNTHESIS VALIDITY:** PRE-REHABILITATION — RETRACTED PENDING REVERIFICATION` (verbatim, all four files) referencing "PI rule #10; cohort defined by DR-2026-05-23."
  - All four slugs are named in `decisions/DR-2026-05-23-cohort-manifest.json`, the cohort manifest for this banner.
  - `decisions/DR-2026-06-10-e2g-reverification-scope.md:6` states verbatim: `"the 68 BPCs at bpc_metadata.evidence_state='RETRACTED-PRE-REHAB'"` and body text: `"68 BPCs carry the PRE-REHABILITATION — RETRACTED PENDING REVERIFICATION banner and evidence_state='RETRACTED-PRE-REHAB' (Phase B.0, Decision 5)... Their original synthesis text remains in the files as historical record but is barred from downstream citation."`
  - The content these four files carry originates from the single fork-cut commit `76a25d9` (2026-08-04, "clean-fork-sqlite-json"), predates any DB-recorded search activity for these slugs (0 `search_executions`, 0 `source_slug_links` for all four), and is dated internally to 2026-03-18/19/29-30 — five months before this repository's earliest real research batch (2026-08-19).
- **Where:** `data/guidebook.db` table `bpc_metadata` (schema has the column, zero population); `decisions/DR-2026-06-10-e2g-reverification-scope.md:6` and body; `decisions/DR-2026-05-23-pre-rehab-banner-cohort-definition.md`; `decisions/DR-2026-05-23-cohort-manifest.json`; the four `bpc_path` files named above.
- **Why it matters:** This is the identical failure shape CLAUDE.md §4 already names for `source_locators` ("a known live defect") applied to a second table: a structurally present, semantically load-bearing table (`bpc_metadata.evidence_state`) that a ratified DR's own prose asserts holds 68 rows in a specific state, but which actually holds none. Any tool, gate, or future session that queries `bpc_metadata` to detect pre-rehabilitation content (rather than grepping the file-layer banner text) will see nothing and treat these slugs as clean. Concretely for batch 04: the orchestrator/agonists are about to write NEW synthesis for these exact four slugs, whose EXISTING synthesis text is formally "barred from downstream citation" per DR-2026-06-10 — but that ban is enforceable today only by a human reading the markdown banner, not by any query against the table the DR's own text says carries it. This is also, independently, a live instance of CLAUDE.md §2(b)'s failure mode: a ratified document (DR-2026-06-10) states a DB fact ("68 BPCs at bpc_metadata.evidence_state=...") that is currently false when checked against the live database.
- **Status:** OPEN
- **Resolution owed:** Either (a) populate `bpc_metadata` for the 68-BPC RETRACTED-PRE-REHAB cohort (`decisions/DR-2026-05-23-cohort-manifest.json` is the source list) via the standard migration write path, making the state DB-checkable and unblocking any gate that should refuse citation of barred synthesis text, or (b) correct DR-2026-06-10's language to state that the RETRACTED-PRE-REHAB state currently lives only in file-layer banners and `bpc_metadata` is not populated. Either way, batch 04 should not treat the pre-existing prose in these four `bpc_path` files as citable without accounting for this banner — that determination belongs to the orchestrator/antagonist, not this tracer.
- **Convergence note (added 2026-09-01, per orchestrator):** This finding independently converges with `decisions/DR-2026-08-19-research-restart-operative-instrument.md` §12.4 trap 12, which separately forbids reading the reasoning doc before step 12 because doing so contaminates the falsification design. Two independent reasons — a DB-integrity gap (this entry) and a methodological blinding requirement (trap 12) — arrive at the same instruction: do not open the four `bpc_path` files before the batch's gates pass. Orchestrator confirms none of the four have been opened. This does not change this entry's class, severity or status; it is recorded so a future reader does not mistake the trap-12 blinding rule for having caused or resolved the `bpc_metadata` emptiness, or vice versa — they are separate facts that happen to license the same caution.

### D04-006 — This session's command log was misfiled into the PREVIOUS session's scratchpad directory by the `open_session()` anchor rule; repaired mid-session by `git mv`, root cause NOT fixed
- **Class:** BUG
- **Severity:** P1 blocks the batch (of the provenance surface itself — batch research work was not blocked, but its own record-of-record was silently corrupted for its first 14+ minutes)
- **Observed:** 2026-09-01, discovered and fixed mid-session by orchestrator; reported to tracer 2026-09-01 ~20:26; independently reconfirmed by tracer 2026-09-01 20:26–20:27
- **What happened:** Every line this session wrote to its command log — from its first Bash call at `2026-09-01T20:12:55Z` through the fix — landed in `scratchpad/session_2026-08-31-od-batch-ratification/commands.jsonl` instead of this session's own directory. **Tracer-verified directly** (read-only, post-fix): the file now at `scratchpad/session_2026-09-01-research-batch-04-accessible-circulation/commands.jsonl` contains, as of this entry, 142 lines, **exactly one distinct `session_id`** (`6a6f63cd-b4d8-5e57-9230-c5afb931a48a`) across all of them, first line timestamped `2026-09-01T20:12:55Z` and last `2026-09-01T20:26:57Z`. `sessions/session_2026-08-31-od-batch-ratification.md` is confirmed absent (tracer-checked: `test -f` fails) — the 08-31 pad was open, carried no lines of its own, and had no session record.
- **Mechanism, tracer-read directly from `.claude/hooks/record-command.py:open_session()`:** the function's own docstring states the design intent verbatim: *"Returning '' rather than guessing is deliberate. The caller then files under the harness session id — a visibly foreign directory name. A WRONG ANSWER MUST BE LOUD."* The actual code is:
  ```python
  openp = [n for n in pads if not (root/"sessions"/f"{n}.md").exists()]
  return openp[-1] if openp else ""
  ```
  This returns `''` only when **zero** open pads exist anywhere — never merely because the true owner can't be identified. With one or more open pads present (the normal case), it always guesses the lexically-last one, silently, contradicting the stated design principle. At `20:12:55Z` this session had not yet created its own pad (a pad is created only after a session's first command — necessarily after the log write that needs to name it), so the newest open pad was `session_2026-08-31-od-batch-ratification` and line 1 went there. From line 2 onward the function's anchor rule — *"a directory whose log ENDS with our sid is our directory. Exact from line 2 onward"* — found that same file now ending with this session's own `session_id` and returned it every time thereafter, including after this session's own pad was created at `2026-09-01 20:16`. **Tracer-confirmed**: evaluating the same `openp[-1]` selection logic right now (read-only Python, matching the function's own filtering) returns `session_2026-09-01-research-batch-04-accessible-circulation` — the self-correction the anchor rule prevented from ever taking effect.
- **Where:** `.claude/hooks/record-command.py:open_session()` (lines ~26–113); the misfiled data was `scratchpad/session_2026-08-31-od-batch-ratification/commands.jsonl` (git status showed it `??` untracked prior to the fix — it did not exist in git at all, meaning no record of the 08-31 session's own commands was ever separately committed under that name).
- **Why it matters:** This is the **third** recurrence of the identical failure shape CLAUDE.md §7 trap 2 already documents twice as FIXED — first under `.claude/session`, then under `sessions/LATEST`. Both those fixes swapped one stale pointer for another; this one replaced the pointer with a derivation, and the derivation still has exactly the failure mode the pointer had: a first-Bash-call race between "which pad is mine" and "does my pad exist yet," resolved by a guess that then locks in and cannot self-correct once it starts locking. The provenance surface this whole hook exists to produce (CLAUDE.md rule 6: "a scratchpad that lives only in context is not a review surface") was, for this session's opening ~14 minutes, silently attributing this session's commands to a different, unrelated, already-closed-in-spirit session's directory — precisely the harm the function's own docstring names ("it corrupts that session's frozen record too") and precisely the failure the loud-`''`-on-uncertainty design was meant to prevent, except the implementation never reaches that branch while any pad is open.
- **Status:** WORKED-AROUND (data repaired, root cause open)
  - **The workaround, tracer-verified:** `git mv scratchpad/session_2026-08-31-od-batch-ratification/commands.jsonl scratchpad/session_2026-09-01-research-batch-04-accessible-circulation/commands.jsonl`. Confirmed via `git status --short`: shows as a clean `R` rename (`RM ... -> ...`), not an add+delete. All 142 lines carry the single `session_id` above, so the move loses nothing and attributes nothing wrongly. The 08-31 pad is retained and still legitimately holds its own `RULINGS.md` (tracer-confirmed present, untouched). Post-move, the anchor now correctly resolves both directions: the 08-31 log no longer ends with this session's sid, and this session's own log does.
- **Resolution owed (explicitly NOT done mid-batch, by the orchestrator's own account — changing a provenance hook's derivation logic while it is recording the batch it would then also be validating is a conflict the orchestrator declined to create):** a change to `open_session()`'s handling of the "no log yet carries our sid" case. Two candidates on record, with their costs stated plainly:
  - *(a)* Let a lexically-newer open pad override the anchor once one exists, so the log follows the session's own directory as soon as it's created. Self-heals the very next command after pad creation; cost is that a single session's log can split across two directories at that boundary (the pre-creation lines stay wherever the opening guess put them unless also migrated).
  - *(b)* Return `''` whenever no existing log carries our sid — i.e., make the opening guess apply only via the anchor, never via `openp[-1]` as a first resort — filing under the raw harness session id as the docstring already says is the intended behavior. Never corrupts another session's directory; the cost is a visibly foreign directory name on every session's first command, which is exactly the loudness the docstring asks for and which nobody has yet had to live with in practice.
  - This tracer takes no position on (a) vs (b) — that is an apparatus decision for the owner/orchestrator (CLAUDE.md §1), not for the record-keeper. Recorded here so the next session that hits this does not treat it as a fresh discovery.

### D04-007 — the anti-fabrication verification check would have examined zero payloads for this batch
- **Class:** BUG
- **Severity:** P1
- **Verification:** ORCHESTRATOR-VERIFIED (one of the three the orchestrator states it independently verified). Tracer independently confirmed the mechanism below via static code read (read-only; `retrieval_log.py` not executed).
- **Observed:** 2026-09-01, by orchestrator
- **What happened:** `retrieval-log/session_2026-09-01-research-batch-04-accessible-circulation/` holds retrieved payloads (tracer-confirmed present: NFBUK, RNIB, RCOT, AOTA documents plus multiple Crossref JSON files) but no `manifest.jsonl`. `retrieval_log.py:_logged_payloads()` reads only the manifest — nothing else — so with it absent, `--verify-authors` prints `EXAMINED: 0` and returns `INDETERMINATE — … it is not a pass`. **Tracer-confirmed by direct read of `scripts/research/retrieval_log.py`**: `_logged_payloads()` is defined at line 159 and called at line 243; the zero-manifest path prints `"  EXAMINED: 0"` at line 246 before falling through to the informational-verdict path.
- **Where:** `retrieval-log/session_2026-09-01-research-batch-04-accessible-circulation/` (no `manifest.jsonl`); `scripts/research/retrieval_log.py` lines 159, 243, 246.
- **Why it matters:** This is exactly failure mode (a) in CLAUDE.md §2 — "a gate that passes having examined nothing" — applied to the specific tool built in direct response to the 2026-08-19 fabrication (CLAUDE.md §2(c)). If this batch's admissions were graded against `--verify-authors` right now, the check would appear to run and would in fact certify nothing, silently.
- **Status:** OPEN — fix planned this session, not yet executed as of this entry
- **Resolution owed:** Orchestrator states the mechanism is confirmed working and the plan is: after admission, run `--backfill` against the scratch DB to populate the manifest (honoured via `DB_PATH`/`GUIDEBOOK_DB_PATH` at `retrieval_log.py:76`), then `--verify-authors`, and require `EXAMINED > 0` before treating the batch as verified. Noted explicitly per the orchestrator: `--backfill` is **honest-but-not-contemporaneous** by its own docstring — it performs a retrieval now, marks it as such in the manifest, and still verifies the already-stored author fields against Crossref's live answer, rather than against the original retrieval moment.

---

### D04-008 — the ratified runbook instructs a write the DB layer and an owner ruling have already retired
- **Class:** CONFLICT
- **Severity:** P2
- **Verification:** ORCHESTRATOR-VERIFIED
- **Observed:** 2026-09-01, by orchestrator; tracer independently confirmed all four cited locations by direct read (read-only)
- **What happened:** `DR-2026-08-19-research-restart-operative-instrument.md` §12.1 step 7 (RATIFIED, operative) instructs `UPDATE search_executions SET … admitted_ref_ids='[…]'`, and §12.4 failure-mode 3 gives an H03/H04 parity query built on that column. Measured against the live tree, all tracer-reconfirmed verbatim:
  - `schemas/search_execution.py:54`: `admitted_ref_ids: Optional[str] = None        # RETIRED - do not write`, with the field comment above it reading: *"RETIRED 2026-08-24. search_admissions is the sole home of which sources a search admitted; this JSON copy is no longer written and its parity checks (H03/H04/H07) are deleted. The field survives because committed data migrations INSERT the column and migrations are append-only."*
  - `scripts/db.py` (~line 394, inside the search-execution insert dict): comment reads *"admitted_ref_ids intentionally NOT written — search_admissions is the sole home (owner ruling 2026-08-24). Column retained because committed data migrations INSERT it and migrations are append-only."*
  - `scripts/tests/test_db_integrity.py` (~line 1019): *"H03/H04 DELETED 2026-08-24 — they policed a dual-write that no longer happens. A parity check between two homes of one fact does not prevent drift; it makes the second home survivable, and therefore permanent."*
  - Only H05 survives (~line 1032): checks `results_admitted` equals the `search_admissions` edge count, and it is blocking and corpus-wide.
- **Where:** `decisions/DR-2026-08-19-research-restart-operative-instrument.md` §12.1 step 7 and §12.4 failure-mode 3 (stale); `schemas/search_execution.py:54`; `scripts/db.py:~394`; `scripts/tests/test_db_integrity.py:~1019,~1032` (current).
- **Why it matters:** This is rule 5 exactly — the JSON column was a second home for a fact `search_admissions` already states, and the owner ruling of 2026-08-24 already resolved which home wins. The ratified runbook is stale on this one point and instructs the losing side. A session following §12.1 step 7 literally would attempt a write the schema comment, the writer's own comment, and the test suite all say is retired.
- **Status:** OPEN
- **Resolution owed:** DR-2026-08-19 §12.1 step 7 and §12.4 failure-mode 3 need a correction noting the 2026-08-24 supersession. Not this tracer's or this batch's call to edit a RATIFIED instrument mid-batch. Orchestrator's working plan: use `log-search --admitted-ref-id`, which writes the junction directly and satisfies H05 at write time, and skip the now-retired enrichment step entirely.

---

### D04-009 — R3's `[UNVERIFIED-QUANT]` escape hatch has only one of its three legitimate carriers reachable from the CLI
- **Class:** BUG
- **Severity:** P2
- **Verification:** ORCHESTRATOR-VERIFIED. Tracer independently confirmed via static read of `scripts/db.py`'s `add-source` argparse block and `_ES_COLS` (not executed — `add-source --help` was not run by the tracer per the hard constraint against invoking `scripts/db.py`).
- **Observed:** 2026-09-01, by orchestrator
- **What happened:** R3 is satisfied by `article_number` OR `pages` OR `notes LIKE '%UNVERIFIED-QUANT%'`. Only `--pages` is reachable through `add-source`. **Tracer-confirmed directly**: the `add-source` subparser (`p_as`, defined `scripts/db.py:1055`, argument list `scripts/db.py:1056–1118`) offers `--url`, `--url-accessed`, `--pages`, `--doi-resolution-outcome`, `--year`, `--title`, `--tier`, `--doi`, `--pmid`, `--jurisdiction`, `--evidence-type`, `--lang-detected`, `--lang-detection-method`, `--metadata-quality`, `--verification-method`, `--verified-by-tool`, `--verification-status`, `--slug`, `--local-ref-id`, `--session`, `--dry-run` — **no `--notes`, no `--article-number`**. `_ES_COLS` (`scripts/db.py:1895`) includes `"notes"` as a permitted column but `article_number` is not in `_ES_COLS` at all, and no CLI flag populates `notes` for this subcommand — the frozenset permits the field, nothing sets it.
- **Where:** `scripts/db.py:1055–1118` (`add-source` subparser), `scripts/db.py:1895–1917` (`_ES_COLS`).
- **Why it matters:** A source with no page numbers has no sanctioned path to carry `[UNVERIFIED-QUANT]` through the writer that is supposed to refuse-rather-than-silently-omit. DR-2026-08-19's own 2026-08-25 supersession note claims "R3, R10, R12 and R13 CAN now be satisfied through the CLI" — measured true only for `--pages`; the note overstates its own fix. CLAUDE.md §4 is explicit that a table or column the CLI cannot reach is a coverage bug to fix, never a licence to hand-write SQL.
- **Status:** OPEN
- **Resolution owed:** Add `--notes` and `--article-number` to the `add-source` subparser (and `article_number` to `_ES_COLS`) so all three R3 carriers are reachable without hand SQL. This is a `db.py` coverage fix, not something to work around by writing SQL directly against the scratch.

---

### D04-010 — the research contract injected into every session's start instructs a write an owner ruling struck four days ago
- **Class:** CONFLICT
- **Severity:** P1
- **Verification:** Antagonist-measured. Tracer independently confirmed by direct read of `governance/research-contract.yaml`, `decisions/DR-2026-08-31-strike-jurisdictional-values-clause.md`, and a read-only DB query.
- **Observed:** 2026-09-01, by antagonist
- **What happened:** `governance/research-contract.yaml` rule R12 — live in the SessionStart payload right now — reads, verbatim (tracer-confirmed at lines 186–192): *"Case studies -> case_studies. Economics -> economics_entries. Code values -> jurisdictional_values. Never leave them in prose notes."* Owner ruling D-0181 (`decisions/DR-2026-08-31-strike-jurisdictional-values-clause.md`, RATIFIED ON CONTACT 2026-08-31, tracer-confirmed present and read in full) struck exactly this instruction from DR-2026-08-19 §12.1 Step 10 on the ground that a 2026-08-12 ruling made `jurisdictional_values` REFERENCE-ONLY — the table names which document to consult, never what it says — and the runbook clause was walking the next research batch into that forbidden write (labelled F-8 in the DR). The strike swept the DR's own runbook clause and did not sweep the contract file, which is a second, independent caller of the same retired instruction. Corroborating measurement, **tracer-reproduced via read-only query**: `jurisdictional_values` holds 109 rows; `value_text`, `value_numeric`, `unit`, `is_code_minimum`, and `source_section` are all 0 non-null across every row — consistent with the table never having been written to in the REFERENCE-ONLY-violating sense the ruling forbids.
- **Where:** `governance/research-contract.yaml` rule R12 (lines ~186–192, unswept); `decisions/DR-2026-08-31-strike-jurisdictional-values-clause.md` (the ruling, which named only the DR's own §12.1 Step 10 clause); `data/guidebook.db` table `jurisdictional_values` (109 rows, 5 named columns all-NULL).
- **Why it matters:** CLAUDE.md rule 4 — "a rename or removal is not done until the callers are swept... a skill is a caller" — is unmet by the very ruling that fixed the original trap. The contract is a caller (it is regenerated into the SessionStart hook by `scripts/generate/research_contract_hook.py` and is literally what every session, including this one, was told at start). As written, R12 still tells a session to write a column an owner ruling forbids, four days after that ruling landed.
- **Status:** OPEN
- **Resolution owed:** Sweep R12 out of (or rewrite it in) `governance/research-contract.yaml`, then regenerate the SessionStart hook via `scripts/generate/research_contract_hook.py --write` (append-only per CLAUDE.md §5's hook-ordering trap — do not insert at index 0). Orchestrator states this is deliberately **not** being done mid-batch: changing the text injected into every session, while this session is itself using that injection, would put the change and its own evidence in one commit.

---

### D04-011 — `db.py`'s own error message states the ref_id minting rule CLAUDE.md names as WRONG
- **Class:** DOC-DRIFT
- **Severity:** P2
- **Verification:** Antagonist-measured. Tracer independently reproduced both the text and the correct value via static read plus a read-only `dbcore` call.
- **Observed:** 2026-09-01, by antagonist
- **What happened:** `scripts/db.py` (~line 1946–1947, the `--ref-id` format-refusal message) tells the user: *"There is no allocator: mint above the source_locators high-water mark, or you will collide with a held identifier (CLAUDE.md §4)."* CLAUDE.md §4 states at length that this exact rule is WRONG — it was corrected 2026-08-25 because minting above `source_locators`' high-water mark yields `REF-00965`, which collides with a live `evidence_sources` row. The correct rule is `dbcore.next_ref_id()`, the union of the high-water mark across every ref_id-bearing table. **Tracer-reproduced directly** (read-only, `dbcore.ref_id_high_water()` / `dbcore.next_ref_id()` against the live DB): high-water mark = **970**, `next_ref_id()` = **REF-00971**. A second refusal message elsewhere in the same file (`scripts/db.py:2511`, inside `insert_locator`'s own error path) states the rule correctly: *"Mint with dbcore.next_ref_id()."*
- **Where:** `scripts/db.py:~1946–1947` (wrong rule, in the general `--ref-id` validator); `scripts/db.py:2511` (correct rule, in `insert_locator` only); `scripts/dbcore.py:263–270` (`next_ref_id()` itself).
- **Why it matters:** The tool's own refusal message — the thing a session reads at the exact moment it needs the correct minting rule — states the superseded, collision-prone version. Only a session that already knows to distrust `db.py` and go read CLAUDE.md §4 (or happens to hit `insert_locator`'s refusal instead) gets the right answer.
- **Status:** OPEN
- **Resolution owed:** Update the `--ref-id` validator's error text at `scripts/db.py:~1946–1947` to point at `dbcore.next_ref_id()`, matching `insert_locator`'s message, so there is one stated rule rather than two.

---

### D04-012 — `dbcore.check_values()` is blind to CHECK constraints written in nullable form, and its own fallback then reintroduces the "live rows as vocabulary" defect it was built to close
- **Class:** BUG
- **Severity:** P2
- **Verification:** Antagonist-measured (including the CLI-level reproduction — `--locator-status DEAD` refused — which the tracer did not attempt, per the hard constraint against running `scripts/db.py`). Tracer independently confirmed the underlying mechanism via read-only code and schema inspection.
- **Observed:** 2026-09-01, by antagonist
- **What happened:** `dbcore.py:348`'s extraction regex is `r"CHECK\s*\(\s*%s\s+IN\s*\(([^)]*)\)" % re.escape(column)` — it requires the literal form `CHECK ( <column> IN (`. Any column whose constraint is instead written as `CHECK (<column> IS NULL OR <column> IN (...))` does not match, and `check_values()` returns `set()`. **Tracer-reproduced directly, read-only**: `search_candidates.locator_status` is declared in `scripts/migrations/057_baseline_2026-08-12.sql:1101` as `TEXT CHECK (locator_status IS NULL OR locator_status IN ('UNVERIFIED','RESOLVED','DEAD'))` — the nullable form. Calling `dbcore.check_values(con, 'search_candidates', 'locator_status')` against the live DB (read-only) returns `set()`, despite the schema plainly declaring three legal values including `'DEAD'`. `check_vocab()`'s documented behavior for an empty declared set is "empty vocabulary means unconstrained... the write proceeds" — but antagonist reports the CLI in practice *refuses* `--locator-status DEAD`, meaning some other code path (a live-row check, per the antagonist) is filling the gap left by the blind regex, which is precisely the "live rows are a sample of a vocabulary, never the vocabulary" failure `check_values()`'s own docstring says it was built to prevent.
- **Where:** `scripts/dbcore.py:329–352` (`check_values()`); `scripts/migrations/057_baseline_2026-08-12.sql:1101` (`search_candidates.locator_status`, the nullable-form CHECK). Antagonist reports ten columns this batch touches are affected in total; tracer confirmed one (`locator_status`) directly and did not enumerate the other nine independently.
- **Why it matters:** The function exists specifically so a refusal can name the real, schema-declared alternative rather than trust a sample of live rows (its own docstring, quoting the 2026-08-25 `search_candidates.disposition`/`OUT-OF-SCOPE` finding). A regex that silently returns empty for a common, legitimate SQL form (`col IS NULL OR col IN (...)`) reopens exactly that hole for every column written that way.
- **Status:** OPEN
- **Resolution owed:** Widen `check_values()`'s regex to also match the `CHECK (<column> IS NULL OR <column> IN (...))` form (and ideally parse CHECK clauses more robustly than a single regex shape), then re-audit which of the ten affected columns were being silently vocabulary-blind. Tracer did not independently verify the "ten columns" figure or attempt to enumerate them.

---

### D04-013 — the pipeline contract is unratified and internally inconsistent with the tool that enforces it
- **Class:** DOC-DRIFT
- **Severity:** P3
- **Verification:** Antagonist-measured. Tracer independently confirmed all four cited facts by direct read (read-only).
- **Observed:** 2026-09-01, by antagonist
- **What happened:** `governance/pipeline-contract.yaml` declares, verbatim (tracer-confirmed lines 2–3): `status: PROPOSED` and `ratified: false` — while CLAUDE.md calls this file "the enforcing single home of the stage ids." Its `spine:` field (line 7, tracer-confirmed verbatim) still reads: `"EvidenceSource (ENT-02) -> BPC entry (ENT-03) -> Specification (ENT-01) -> Item (ENT-08) -> render"` — the pre-2026-08-27 four-hop chain, not the six/seven-stage spine CLAUDE.md's pipeline section now describes. Separately, `tools/pipeline_completeness.py` declares `STAGES = ["base", "research", "evidence", "judgment", "synthesis", "specification", "render"]` at line 37 (seven entries, tracer-confirmed) but renders the phrase **"the five pipeline stages"** at line 682 and **"The five stages at a glance"** at line 694 (both tracer-confirmed verbatim, exact line numbers). `pipeline_completeness_fresh` is a blocking check (tracer-confirmed against `governance/check-registry.yaml` during this session's own baseline pass), so this page is regenerated and re-emits the wrong stage count on every run rather than being a one-off stale artefact.
- **Where:** `governance/pipeline-contract.yaml:2-3,7`; `tools/pipeline_completeness.py:37,682,694`.
- **Why it matters:** Two separate instances of CLAUDE.md §2(b)'s named failure mode ("prose that contradicts the database... generate from the DB, or stamp with a drift warning") co-existing in the one file this project treats as the pipeline's canonical enforcement surface: an unratified contract asserting authority CLAUDE.md defers to, and a rendered page whose own header count (five) contradicts its own code constant three lines above it (seven).
- **Status:** OPEN
- **Resolution owed:** Ratify or retire `governance/pipeline-contract.yaml` (its `status`/`ratified` fields should reflect one or the other, not sit in a "PROPOSED" state CLAUDE.md treats as authoritative); update its `spine:` field to the current stage chain; and change `tools/pipeline_completeness.py`'s rendered prose at lines 682/694 to derive the stage count from `STAGES` (len 7) rather than a hand-written "five," consistent with CLAUDE.md §2(b)'s ban on hardcoded counts in derived documents.

---

### D04-014 — one foreign-key back-edge in the migration-emission table order
- **Class:** DATA
- **Severity:** P3
- **Verification:** Antagonist-measured. Tracer independently confirmed both index positions and the underlying FK by direct, read-only inspection.
- **Observed:** 2026-09-01, by antagonist
- **What happened:** `evidence_population_match.gap_id` carries `REFERENCES gaps(gap_id)` (tracer-confirmed, `scripts/migrations/057_baseline_2026-08-12.sql:203`). In the FK-ordered table list used by `scripts/research/emit_batch_sql.py` — which the file's own comments show was consolidated into `dbcore.WRITABLE_TABLES` on 2026-08-25 specifically so no table could again be "writable but invisible to capture" — `evidence_population_match` sits at **index 7** and `gaps` at **index 12** (tracer-reproduced by direct enumeration of `dbcore.WRITABLE_TABLES`, read-only). A parent (`gaps`) is emitted after a child that references it (`evidence_population_match`), inverting the ordering the list exists to guarantee ("a parent is always emitted before anything that references it, so the migration applies cleanly even with foreign_keys enforcement on" — `emit_batch_sql.py`'s own header comment).
- **Where:** `scripts/dbcore.py` (`WRITABLE_TABLES`, indices 7 and 12); `scripts/migrations/057_baseline_2026-08-12.sql:203` (the FK declaration); `scripts/research/emit_batch_sql.py` (the consumer, header comment on table ordering).
- **Why it matters:** A `search_candidates`/`evidence_population_match` row that references a `gaps` row created in the *same* research batch would be emitted before its parent exists, and the resulting migration SQL would fail (or silently violate ordering) under foreign-key enforcement.
- **Status:** WORKED-AROUND
  - **Workaround adopted (antagonist):** for this batch, either leave `--gap-id` NULL on any new `evidence_population_match` row, or ship the referenced gap in an earlier, already-applied migration so it is never a same-batch forward reference.
- **Resolution owed:** Move `gaps` earlier than index 7 in `dbcore.WRITABLE_TABLES` (or otherwise re-derive the ordering from the actual FK graph rather than a hand-maintained list) so this class of same-batch forward reference cannot recur. Not attempted this session — batch 04 does not currently need a same-batch gap+match pairing, per the adopted workaround.

---

## Summary
| ID | Class | Severity | Status |
|---|---|---|---|
| D04-001 | DOC-DRIFT | P3 | OPEN |
| D04-002 | DATA | P2 | OPEN (inherited) |
| D04-003 | DATA | P2 | OPEN (inherited) |
| D04-004 | DOC-DRIFT | P3 | OPEN |
| D04-005 | DATA | P2 | OPEN |
| D04-006 | BUG | P1 | WORKED-AROUND |
| D04-007 | BUG | P1 | OPEN (fix planned this session) |
| D04-008 | CONFLICT | P2 | OPEN |
| D04-009 | BUG | P2 | OPEN |
| D04-010 | CONFLICT | P1 | OPEN |
| D04-011 | DOC-DRIFT | P2 | OPEN |
| D04-012 | BUG | P2 | OPEN |
| D04-013 | DOC-DRIFT | P3 | OPEN |
| D04-014 | DATA | P3 | WORKED-AROUND |
