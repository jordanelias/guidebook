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

---

## Summary
| ID | Class | Severity | Status |
|---|---|---|---|
| D04-001 | DOC-DRIFT | P3 | OPEN |
| D04-002 | DATA | P2 | OPEN (inherited) |
| D04-003 | DATA | P2 | OPEN (inherited) |
| D04-004 | DOC-DRIFT | P3 | OPEN |
| D04-005 | DATA | P2 | OPEN |
