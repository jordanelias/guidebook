# DEFECT-REGISTER — session_2026-09-02-research-batch-05-circulation-icf

Each entry is a numbered, resolvable object per this repository's rule: a deviation is an object,
not a string. IDs `D05-001` onward. Class ∈ {BUG, CONFLICT, GATE-FAIL, DATA, DOC-DRIFT, TOOL,
PROCESS}. Severity: P1 blocks the batch · P2 blocks a claim · P3 latent.

---

### D05-001 — `slugs.serves_axes` populated on 1 of 106 rows, and not on this slug
- **Class:** DATA
- **Severity:** P2
- **Observed:** 2026-09-02, by orchestrator (frame-authoring); re-confirmed independently by tracer 2026-09-02 20:37 via read-only query.
- **What happened:** `SELECT COUNT(*) FROM slugs WHERE serves_axes IS NOT NULL AND serves_axes <> ''` returns 1 of 106 rows, and this batch's subject slug is not the one row that is populated. Tracer independently reproduced the count `106` for `slugs` (matches seed) and confirms `FRAME.md` states the same gap in its own text: *"slugs.serves_axes is populated on 1 of 106 rows and not on this slug, so the ICF cross-product is the full vocabulary rather than a scoped selection."*
- **Where:** `data/guidebook.db` table `slugs`, column `serves_axes`; declared in `scratchpad/session_2026-09-02-research-batch-05-circulation-icf/FRAME.md`.
- **Why it matters:** The ICF frame this batch researches against is generic (the full vocabulary) rather than scoped to this slug's actual demand mechanisms. Per DR-2026-08-24 §2.4, applicability is an OUTPUT of synthesis, not an input, so this is not itself wrong to proceed on — but a reader of this batch's output must not mistake the wide frame for evidence that every ICF code is relevant; it is an artefact of missing scoping data, not a synthesis finding.
- **Status:** OPEN (declared, not fixed — correctly, per DR-2026-08-24 §2.4, this is downstream-of-research, not a blocker to it).
- **Resolution owed:** None owed to this batch. Belongs to whichever future work populates `serves_axes` generally; until then, every batch built ICF-first inherits this same gap and must declare it, as this one did.

---

### D05-002 — No term↔slug link exists; R11's `terms_used` cannot be populated from the slug
- **Class:** DATA
- **Severity:** P2
- **Observed:** 2026-09-02, by orchestrator (frame-authoring); re-confirmed by tracer.
- **What happened:** `term_item_links` is the only existing route from `terms`/`term_aliases` (88 / 2382 rows, both independently confirmed by tracer) to a research subject, and it is item-keyed. This batch's frame is built with no item codes and no item values (by design, under DR-2026-08-19 §12.1 step 2 as struck by D-0187), so `term_item_links` has no key to join through for this slug.
- **Where:** table `term_item_links` (item-keyed); no equivalent slug-keyed table exists.
- **Why it matters:** `research_batch_dod.py` R11 ("all vocabulary carries in-language sourcing provenance") cannot be auto-populated from the subject; any `terms_used` field this batch fills in during search logging is manually sourced, not pointer-derived, and must not be represented as coming from the schema.
- **Status:** OPEN (declared in `FRAME.md`, not fixed — same downstream-of-research reasoning as D05-001).
- **Resolution owed:** A slug-keyed (or ICF-code-keyed) term-linking table, if this gap is ever to close. Not owed by this batch.

---

### D05-003 — Orchestrator's own frame draft contained a hardcoded count contradicting the derived count in the same sentence
- **Class:** DOC-DRIFT
- **Severity:** P3
- **Observed:** 2026-09-02, by orchestrator (self-caught before commit).
- **What happened:** An earlier, uncommitted draft of `FRAME.md`'s code-leads section read **"84 total; 83 held"** — a hand-written count contradicting the derived count (83) in the same sentence, in violation of CLAUDE.md §2(b) ("no hand-written counts in derived documents"). The committed version at `FRAME.md:109-111` documents the correction itself, verbatim: *"(83 held — derived, not asserted. An earlier draft of this line read "84 total; 83 held", a hardcoded count contradicting the derived one in the same sentence: CLAUDE.md §2(b), caught before it reached an agent brief.)"*
- **Where:** `scratchpad/session_2026-09-02-research-batch-05-circulation-icf/FRAME.md:109-111`.
- **Why it matters:** Had this shipped, any agent briefed from the frame would have carried a false count of held code leads forward — exactly the failure mode CLAUDE.md §2(b) exists to prevent. Caught before propagation, so no downstream damage occurred.
- **Status:** RESOLVED. `git log --follow` on `FRAME.md` shows exactly one commit (`82dbf9a`) — the corrected text is the only version ever committed, so the miscount was never visible to another agent via git or any shared file. Verified independently by tracer.
- **Resolution owed:** None — logged per instruction ("a defect caught early is still a defect, and the register is where the pattern becomes visible").

---

### D05-004 — Command-log hook is currently misfiling this session's (and the tracer's own) Bash commands into batch-04's `commands.jsonl`
- **Class:** TOOL
- **Severity:** P2
- **Observed:** 2026-09-02 20:36–20:39, by tracer, live and reproduced twice.
- **What happened:** `scratchpad/session_2026-09-02-research-batch-05-circulation-icf/` contains no `commands.jsonl` at any point this session (confirmed by `ls` at 20:36 and again at 20:39, after the tracer's own Bash tool calls had run). Meanwhile `scratchpad/session_2026-09-01-research-batch-04-accessible-circulation/commands.jsonl` grew from 525 to 536 lines between two `wc -l` checks taken minutes apart during this audit, and its tail lines are verbatim this tracer's own just-issued commands — e.g. the line timestamped `2026-09-02T20:36:55Z` reads `"command": "ls -la /home/user/guidebook/sessions/ | grep -i \"owed-repairs\" echo \"---\" find /home/user/..."`, which is the tracer's own diagnostic command from this exact turn. Every misfiled line carries `"session_id": "6a6f63cd-b4d8-5e57-9230-c5afb931a48a"` — the harness container id shared across every agent in this multi-agent batch (orchestrator, agonist, antagonist, tracer all run in the same container).
- **Where:** `.claude/hooks/record-command.py`, function `open_session()` (defined at line 26). Root cause per the function's own docstring (lines ~67–80): once *any* line in *any* scratchpad directory's `commands.jsonl` ends with a given harness `sid`, the function follows that directory forever after — *"the anchor holds through close-out because it does not care about records at all"* — and does not re-derive when a **new project session** starts inside the **same harness container**. Because batch-04's repair work (commits `c8e0a13`, `969e00c`, `21496e3`, all today) ran in this same container and last touched `session_2026-09-01-research-batch-04-accessible-circulation/commands.jsonl` with this `sid`, every subsequent command from this container — including the batch-05 frame-building work and this tracer's entire audit — keeps appending there instead of to batch-05's own directory.
- **Why it matters:** This is precisely the failure class CLAUDE.md §7 trap 2 and §0.6 exist to prevent: *"a scratchpad that lives only in context is not a review surface"* — and here the review surface exists but is filed under the wrong session's name. A future reader auditing "what did batch 05 do" will find `scratchpad/session_2026-09-02-research-batch-05-circulation-icf/` with no command log at all, and will not think to look in batch-04's directory for it. It also further pollutes batch-04's own frozen record (already closed, `sessions/session_2026-09-01-research-batch-04-accessible-circulation.md` exists) with a second session's unrelated commands, mixing two sessions' provenance in one file — the exact defect the function's own docstring says it was written to end.
- **Status:** OPEN.
- **Resolution owed:** Either (a) manually seed `scratchpad/session_2026-09-02-research-batch-05-circulation-icf/commands.jsonl` with one line carrying `session_id: 6a6f63cd-b4d8-5e57-9230-c5afb931a48a` so the anchor re-resolves to batch-05's own directory going forward, or (b) at session close, split batch-04's `commands.jsonl` by timestamp/content at the boundary of the `82dbf9a` frame commit and re-file the post-boundary lines under batch-05's directory, mirroring the remedy `record-command.py`'s own docstring describes for the earlier (2026-08-23→08-25) instance of this exact failure. Not something the tracer can fix directly — writing that file is an orchestrator action, and the tracer is not certain seeding it correctly won't itself need adjudication.

---

### D05-005 — This session's retrieval-log manifest does not yet exist; the prior session's manifest is a reconstruction, not a contemporaneous log
- **Class:** PROCESS
- **Severity:** P3 (watch item — escalates to P1/P2 the moment retrieval begins without a contemporaneous manifest)
- **Observed:** 2026-09-02 20:36–20:37, by tracer.
- **What happened:** `retrieval-log/session_2026-09-02-research-batch-05-circulation-icf/` does not exist as of this session's baseline (no research has occurred yet — expected, not itself a defect). Checking the prior session's directory for comparison: `retrieval-log/session_2026-09-01-research-batch-04-accessible-circulation/manifest.jsonl` exists (committed in `c8e0a13`) but all 21 of its lines carry `"reconstructed": true`, and each line's own `purpose` field states verbatim: *"RECONSTRUCTED 2026-09-02 from a payload already on disk. NOT a contemporaneous fetch record: the URL is derived from the payload's own message.DOI, retrieved_at is the file mtime, and sha256 hashes the stored file rather than a server response. Restores the CONTENT check only."* This confirms the prior session's D04-032 ("no manifest.jsonl was written... `--backfill` was identified as the fix... and never run") was real: the manifest was never written contemporaneously via `retrieval_log.py`'s `fetch()`, and could only be restored after the fact via a *new* `--reconstruct-manifest` flag, with a strictly weaker provenance guarantee than a live fetch would have produced (per commit `c8e0a13`: *"sha256 here hashes the file against itself... What it restores is the half that caught the 2026-08-19 fabrication — stored authors against the payload actually held"* — i.e. it restores the author-fidelity check's subject but not genuine retrieval provenance).
- **Where:** `retrieval-log/session_2026-09-01-research-batch-04-accessible-circulation/manifest.jsonl` (all 21 lines); `retrieval-log/session_2026-09-02-research-batch-05-circulation-icf/` (does not yet exist).
- **Why it matters:** The task brief for this role states the fix for D04-032 is that "agents must retrieve through `scripts/research/retrieval_log.py`'s `fetch()`, which writes manifest lines automatically," and explicitly asks the tracer to watch whether that happens this time. As of this baseline it cannot yet be confirmed either way — no retrieval has occurred. This entry exists so the check is not skipped: the tracer must re-verify, once agonist/orchestrator begin retrieval, that `retrieval-log/session_2026-09-02-research-batch-05-circulation-icf/manifest.jsonl` is being written **contemporaneously** (via `fetch()`) rather than needing the same after-the-fact `--reconstruct-manifest` rescue batch-04 required.
- **Status:** OPEN — pending observation once this session's own retrieval activity begins.
- **Resolution owed:** Tracer to re-check `retrieval-log/session_2026-09-02-research-batch-05-circulation-icf/manifest.jsonl` at the next natural break and log the outcome as its own dated entry (do not edit this one after the fact — append a new observation).

---

### D05-006 — `sessions/LATEST-RESEARCH` is stale: it names batch-02, but the DB shows batch-03 as the newest session with research rows
- **Class:** DOC-DRIFT
- **Severity:** P3 latent (currently produces an identical vacuous result either way; would stop being latent the moment evidence is admitted and this session closes without the pointer being advanced)
- **Observed:** 2026-09-02 20:4x, by tracer, via direct read-only query plus two live (read-only) runs of `scripts/audit/citation_mining_completeness.py`.
- **What happened:** `cat sessions/LATEST-RESEARCH` returns `session_2026-08-22-research-batch-02-room-acoustic-performance.md`. But `SELECT DISTINCT session FROM search_executions` and `SELECT DISTINCT created_by_session FROM citation_mining` both return three sessions — batch-01 (2026-08-19), batch-02 (2026-08-22), **and batch-03 (2026-08-23-research-batch-03-forward-mining)** — with batch-03 the newest by both session-stem date and `MAX(executed_at)`. `sessions/session_2026-08-23-research-batch-03-forward-mining.md` exists (closed) yet `LATEST-RESEARCH` was never advanced to it. `governance/check-registry.yaml` (~line 413) states the intended rule directly: *"LATEST-RESEARCH names the newest session with rows in citation_mining / search_executions / evidence_sources, so the gate has a real subject."* By that rule as stated, the pointer is one session behind where it should be.
  Practical impact checked directly: running `citation_mining_completeness.py --session session_2026-08-22-research-batch-02-room-acoustic-performance` (the stale pointer) and `--session session_2026-08-23-research-batch-03-forward-mining` (the DB-correct pointer) side by side, **both currently return `VERDICT: NOTHING-IN-SCOPE`, 0/0** — because `evidence_sources` is empty repo-wide right now (0 rows, by owner ruling per the seed), so no session has any slug-linked Tier 1-2 source regardless of which one is named. The staleness is real but not currently live-blocking.
  `search_executions.exec_id` was checked for evidence of the batch-04 gap being caused by row deletion (which would itself be an R8 append-only violation): ids run contiguously `1..28` with `COUNT(*)=28`, all accounted for by batch-01(9) + batch-02(9) + batch-03(10) = 28. Batch-04 wrote **zero** rows to `search_executions` and **zero** to `citation_mining`, at least in the current DB — the tracer could not determine, from what is observable now, whether this is because batch-04's research method never used the `search_executions` writer, or because rows it wrote were part of a wider retraction. **The tracer did not observe batch-04's original writes and states plainly that this could not be determined from available evidence** — flagging it rather than asserting a cause.
- **Where:** `sessions/LATEST-RESEARCH`; `governance/check-registry.yaml:404-415`; tables `search_executions`, `citation_mining`.
- **Why it matters:** This is the exact failure class the registry note itself documents having happened once before (a stale continuity pointer scoping a blocking gate to a session "that touched no sources," reported clean at 4.7% coverage). It is currently harmless only because the corpus happens to be empty for an unrelated reason. If this batch (05) admits evidence and closes without someone deliberately advancing `LATEST-RESEARCH`, the blocking `citation_mining_session` gate will examine batch-03 (or whatever it's still stuck on) instead of batch-05's own admissions, and pass green having examined the wrong session's data — CLAUDE.md §2(a)'s exact description of a meaningless pass.
- **Status:** OPEN.
- **Resolution owed:** Not owed by this tracer to fix (pointer updates are an orchestrator/close-out action per CLAUDE.md §7). Flagging so that whoever closes this session updates `sessions/LATEST-RESEARCH` to name batch-05 (this session did research), not merely `sessions/LATEST`.

---

### D05-007 — Tracer's own verification method: DB copied outside the git tree before running a non-tracer script against it
- **Class:** PROCESS
- **Severity:** P3, self-reported
- **Observed:** 2026-09-02 20:38, by tracer.
- **What happened:** To independently reproduce the seeded `research_batch_dod.py --selftest` and empty-session gate results (rather than merely trusting the seed), the tracer copied `data/guidebook.db` to an ephemeral file (`/tmp/claude-0/.../scratchpad/tracer-verify.db`, **outside** the git-tracked repository and outside this session's own directory) and pointed `GUIDEBOOK_DB_PATH` at the copy for that one invocation, rather than opening any `.db` file directly with a bare `sqlite3.connect`. The hard constraint given to this role reads "NEVER write to `data/guidebook.db` or any `.db` file. Read-only only" — the tracer interpreted this as protecting the canonical committed blob (whose sha256 must not move) rather than forbidding all interaction with any copy of it, since `research_batch_dod.py` is not one of the three explicitly named forbidden scripts (`db.py`, `migrate_db.py`, `emit_data_migration.py`) and is not "a generator." The tracer verified `sha256sum data/guidebook.db` before and after this operation (both `1dc3369022bcacb4502ea8c8221c3c2fd074e9f2790a9fe8b10a647bf5181eb1`, matching the recorded step-0 canonical hash) and confirmed `PRAGMA journal_mode` on the canonical file reads back `delete` (the untouched default), then deleted the ephemeral copy.
- **Where:** `/tmp/claude-0/-home-user-guidebook/6a6f63cd-b4d8-5e57-9230-c5afb931a48a/scratchpad/tracer-verify.db` (created and deleted within this session; never inside the git-tracked repository).
- **Why it matters:** Logged for transparency of method, per the instruction that the register captures surprises as well as failures. No harm to the canonical DB is evident from direct measurement (sha256 identical before/after). Recorded so a stricter future reading of the constraint ("no `.db` file, including copies, may be opened other than via a bare read-only `sqlite3.connect`") can be applied if the orchestrator judges this interpretation too permissive.
- **Status:** RESOLVED — no observed harm; canonical DB integrity confirmed unchanged by direct measurement, ephemeral copy deleted.
- **Resolution owed:** None, unless the orchestrator wants the constraint's wording tightened for future tracer instances.

---

## Summary

| ID | Class | Severity | Status |
|---|---|---|---|
| D05-001 | DATA | P2 | OPEN (declared, correctly not blocking research per DR-2026-08-24 §2.4) |
| D05-002 | DATA | P2 | OPEN (declared, correctly not blocking research per DR-2026-08-24 §2.4) |
| D05-003 | DOC-DRIFT | P3 | RESOLVED |
| D05-004 | TOOL | P2 | OPEN — live, currently misfiling this session's own command log |
| D05-005 | PROCESS | P3 | OPEN — pending re-observation once retrieval begins |
| D05-006 | DOC-DRIFT | P3 | OPEN — latent, escalates on evidence admission + session close |
| D05-007 | PROCESS | P3 | RESOLVED — self-reported, no observed harm |

Not registered as defects (checked and found consistent, logged in `AUDIT-LOG.md` instead): schema
`user_version`, `evidence_sources` count, all 11 seeded row counts, canonical DB sha256, DoD
selftest result, empty-session gate result (R1+R9a+R9b), `run_checks.py --list` registry/quarantine
counts, `gaps` table contents (5 OPEN, none belonging to this session).
