# Session Handoff — Accessible Built Environments Guidebook
**2026-06-11 15:45 UTC · repo `jordanelias/guidebook` @ `main` = `93c017f` (20 commits ahead of baseline `928c438`) · worktree clean · DB v24**

This is the clean resume document. Per-stage detail logs live in `SESSION-HANDOFF-2026-06-09.md` (running log) and the per-stage summaries (`2.5-…`, `4.2-…`, `4.3-phase-e-execution-plan.md`).

---

## 1. Where we are

Stages **1.x, 2.0–2.5, and 4.2 are complete and pushed.** Stage **4.3 (Phase E synthesis) is planned and gate-prepped but not started** — it is blocked on two owner decisions (§4). The next session does a short gate-closure run, then resumes the existing synthesis pilot. No synthesis content has been written yet; no entity data was touched in the most recent work.

**Execution model (since CI was deleted this session):** build → verify with my own checks (rebuild + invariants + tests + the level-2 audits) → commit → **push directly to `origin/main`**. The blocking CI gates (`ci.yml`/`audit.yml`) are gone; auxiliary scheduled jobs (`verify-urls`, `resolve-dois`, a `vetting-surface-regen`) **still run and push to `main`**, so every push must be rebase-aware. `git push origin main` works as-is (embedded credential); do **not** add a Bearer header. Commits use `--no-verify`. PAT at `/mnt/project/GitHub_pat` (strip backticks); always redact in output.

---

## 2. Verified current state

- **Repo:** `HEAD = origin/main = 93c017f`, synced, worktree clean, 20 commits ahead of baseline.
- **DB (`data/guidebook.db`, tracked, v24):** evidence_sources 640 · evidence_source_authors 1244 · items 92 · slugs 82 (all ACTIVE) · connections 273 · gaps 296 · populations 22. `scope` NULL = 0, tier inconsistencies = 0. Ledger reconciled: `migrate_db` reports **no pending** (186 data + 13 schema migrations); `--rebuild` reproduces the 7 core invariants (but **not** evidence_source_authors — see §5 gotcha).
- **Phase-E eligibility (rule #6 gate):** **67 of 82** ACTIVE slugs fully eligible now; 14 zero-source (research-first); 1 blocked on a single residual source.
- **Pilot:** `references/bpc-reasoning/room-acoustic-performance.md` exists, headed `Status: PILOT (Phase E.1 Track 3)`, RT60 rule-#9 walk at Pass 1 (steps 1–3), 7 `reasoning_doc_citations` rows (one is `NOT-FOUND`, to resolve).
- **parts/v10:** 15 reproducible files regenerated from the DB by `scripts/generate_parts.py` (stub mode); 21 pre-rehab drafts archived to `parts/_archived/v10-predraft-2026-04-23/`.

---

## 3. What this session shipped (20 commits, all pushed)

Foundation + machinery (Stages 1.x, 2.0–2.5):
- Evidence-hierarchy reconciliation to the ratified ladder (D-A/D-D/D-E); `validate_reasoning` made status-aware (OPUS-PENDING); migration-ledger backfill per DR-2026-05-28 step 2 (`29e0133`).
- Phase A: search_languages → 19 langs; search_coverage → 46 jurisdictions; `items.bpc_source_slug` populated; `lang_jur_map` table added (empty).
- **Stage 2.2–2.4:** consolidated directness model; `evidence_cell_state` + `convergence_assessment` built (migration 024, item×population×scale grain); `validate_evidence_state` wired (pending⇒gap enforcement). Bootstrap denominators DB-derived.
- **Stage 2.5:** tier-consistency sweep — 17 NULL-scope rows resolved (11 tier fixes + 6 evidence_type corrections), 0 inconsistencies. *Owner-review residue:* the 6 type-changes + 5 Phase-B flags in `2.5-resolution-table.md`.

Stage 4.2 (A.12 reassembly):
- `scripts/generate_parts.py` (stub/full modes, idempotent via DB-fingerprint) + 14-test suite. Closes R3-b.
- Committed DB forward-migrated v21→v24 + ledger reconciled (R3-c), 1244 authors preserved; stale parts/v10 retired + regenerated.
- **Finding:** `architecture/page-templates.md` is the **4.4 webpage** spec against a webpage schema that does not exist in the canonical DB — flagged for 4.4 (build schema or rewrite templates).

Stage 4.3 prep (this session's tail):
- **Plan delivered:** `4.3-phase-e-execution-plan.md` v1.1 (full reads of Phase E + all four protocol skills + live preflight).
- **DRs ratified + filed:** `DR-2026-06-10-synthesis-model-floor` (rule #2 = capability floor "Opus-class or above"; Fable 5 qualifies) and `DR-2026-06-10-e2g-reverification-scope` (full re-synthesis; prior retracted prose = claim inventory only) + 3 rule-#11 attestations; v10.15 rule-#2 clarification queued for owner paste. Commit `93c017f` carried `[DOCTRINE: 3da73bd]`.

---

## 4. BLOCKED ON YOU — decisions gating Stage 4.3 execution

1. **D-4.3-H — `evidence_source_authors`/`pipeline_runs` reproducibility posture** (this is the real Stage 3.1 / G1; the planned "capture 165 rows as a migration" is **categorically wrong** per ratified DR-2026-05-28 — those rows are genuine job enrichment; capture/rebuild would delete correct data). Pick: **(3a, recommended)** declare these "job-owned" tables exempt from the reproducibility contract + scope the invariant script to the 7 core invariants + align architecture wording; **(3b)** have the source-verification job emit a snapshot migration per run.
2. **Scholarly-connector approval (D-4.3-C).** The carve-out is accepted, but GAP-286 records the connectors returning "No approval received" — they must be **enabled in your claude.ai settings** before PMP's strict searches and E.2b retrieval can use them.

Accepted but owner-paste-pending: the v10.15 rule-#2 clarification (goes live only when you paste it into claude.ai → Project Settings). D-4.3-D/E/F/G accepted per your instruction.

---

## 5. Next session — exact resume sequence

Start fresh (context). Bootstrap is exempt for governance/tooling but run it before content work. Then, in order:

1. **G4 — protocol-drift doc fixes** (small, safe, must precede synthesis): (a) `reasoning-doc-citations` pre-check → add `COMPLETE-STATUTORY` (else all 328 statutory sources wrongly disqualified); (b) `multilingual-research` completeness thresholds 24→46 jurisdictions (23/46 Co-1, 31/46 Tier-5 per D-4.3-G); (c) sweep stale "Sonnet 4.6/Opus 4.6" model pins → "Opus-class or above" per DR-A. Reconcile in `references/skill-registry.md`.
2. **G2** — resolve or CLOSED-DELETE the 1 remaining `AUTHOR-TITLE-ONLY` source (blocks the methodology slug).
3. **G3** — Stage 4.1 re-attestation sweep against doctrine `3da73bd`. **`[GAP]`: the Stage 1.1 re-attestation list was not located in `governance/` or `decisions/` — locate or reconstruct first.** GAP-265/269 close inside W1 synthesis, not on paper (D-4.3-F).
4. **G5** — populate `lang_jur_map` (empty) from the multilingual skill's language↔jurisdiction text (mechanical migration).
5. **D-4.3-H execution** once you rule 3a/3b (governance + invariant-script scope, not an entity migration).
6. **Pilot resume** — `room-acoustic-performance`: resolve the `NOT-FOUND` rdc row, finish the RT60 walk (steps 4–9 + sub-rule-3), then the first PMP walks. **Inline owner review after each block** (Track-3 mandate). Calibrate the per-slug cost model from the pilot before scaling to waves W1→W-last (plan §6).

The per-BPC protocol, schema bindings, wave order, verification battery, risks, and sizing are in `4.3-phase-e-execution-plan.md` §§4–11.

---

## 6. Operating model + gotchas a resuming session MUST know

- **Do NOT `--rebuild`-and-replace the committed DB.** Per DR-2026-05-28: a from-scratch rebuild yields 1079 authors vs the committed 1244 — the 165-row delta is genuine source-verification-job PubMed enrichment, not reproducible from migrations. Rebuilding + replacing "would silently delete 167 rows of correct data." To bring the committed DB forward, **forward-migrate in place** (`GUIDEBOOK_DB_PATH=… migrate_db.py`), never `--rebuild` over it.
- **Every DB write ships as a data migration** via `scripts/emit_data_migration.py` (forward-only, idempotent), applied in place and committed with the touched files. No direct writes.
- **Rule #11 on `decisions/`, `references/bpc-reasoning/`, `references/connection-reasoning/`, synthesis-bearing `sessions/`:** commit message needs `[DOCTRINE: <7-char-sha>]` **before** the trailing `[YYYY-MM-DD HH:MM]` (current doctrine SHA = `3da73bd` = `HEAD:governance/mission-and-epistemics.md`), **and** an `attestations/<artifact-slug>.json` validating against `schemas/attestation.schema.json`.
- **Commit-message regex:** `^[a-z][a-z0-9_-]+:\s+.+\s+\[\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}\]$`. Timestamp LAST, via `date -u`.
- **Synthesis routing (rule #2, per DR-A):** Opus-class-or-above may write `best_practice_synthesis`; Fable 5 qualifies. Facts-pass work is unrestricted.
- **Verification battery** (replaces deleted CI): `validate_reasoning` / `validate_bpc` / `validate_evidence_state` per pass; `research_protocol_audit` / `pmp_audit` / `reasoning_doc_citations_audit` / `adherence_log_audit` / `audit_evidence_metadata` per session (all exit 0 before close); `--rebuild` 7-invariant check + `generate_parts.py` regen per wave. Terminal proof of 4.3 done: `generate_parts.py --mode full` exits 0.
- **userPreferences still in force:** effort=max, full reads of referenced docs, audit tags at stage boundaries, honest_findings (never manufacture / never sham-clear; flag-don't-force consequential actions), context_window 1M (don't ration under 750k), no flattery, MCP connectors off by default (except the ratified scholarly carve-out for 4.3).

---

## 7. Open gaps / owner-pending residue

- `[GAP]` Stage 1.1 re-attestation list not located (blocks G3/4.1).
- `[GAP]` "Multilingual Research Protocol v4" + the 14-language Keyword Compendium not located on disk (E.2b pre-run inputs) — locate or author before the first multilingual run.
- `[GAP]` `lang_jur_map` empty (G5 fixes); A.3 role-taxonomy population still owner-pending.
- Stage 2.5 owner-review: 6 evidence_type changes + 5 Phase-B flags (`2.5-resolution-table.md`).
- 4.4 finding: `page-templates.md` schema drift (webpage schema absent) — resolve at 4.4.
- Live scheduled jobs write `data/guidebook.db` and push to `main` (D-4.3-H decides whether to formalize/exempt or pause them during waves).
- `[DRIFT: commit-timestamp]` some earlier session commits used the `2026-06-09` session label rather than real UTC (now `2026-06-11`); future commits use `date -u`.
