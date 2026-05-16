# session_2026-05-15a — governance reconciliation

**Date:** 2026-05-15
**Predecessor:** `session_2026-05-13b-evidence-verification-methodology.md`
**Intermediate artifact:** `sessions/handoff-next-session.md` (written 2026-05-14, partial state preservation but not a session record per `<session_close>`)
**Focus:** Reconcile audit trail between session_2026-05-13b close (2026-05-13 20:38) and now. Two days of work landed on `main` without a corresponding session record; bootstrap pattern bug surfaced separately. Both close in this session.
**PI:** v10.11 (live); v10.12 drafted here.
**Effort:** max (per preferences default).

---

## Scope

This is a governance session, not a content session. PI rule #6 strict sequential B-before-E is unaffected; no BPC work occurred. The session is bootstrap-exempt-adjacent per `<bootstrap_pattern>` ("pure governance work on PI / preferences / architecture themselves") but bootstrap was run anyway to surface the state gap that prompted the session.

## Bootstrap findings — the prompts

Bootstrap printed two unexpected lines:

1. `Skills: 0 registered` — `grep -c '^### '` returns 0 against `references/skill-registry.md`. Registry uses `##` section headings plus a code-block listing for active skills, not `### ` per-skill subheadings. The pattern has been broken since v10.6+ refactored the registry shape; status report has silently misreported skill count.
2. `session: session_2026-05-13b-evidence-verification-methodology.md` — `sessions/LATEST` had not been bumped despite ~51 commits since that session closed.

The second prompt triggered a fuller reconciliation pass.

## Reconciliation — 51 commits since 2026-05-13b close

Grouped by date.

### 2026-05-13 (post-session-close, 5 commits)

| Commit | Subject |
|---|---|
| `0297db5a` | `reasoning_doc_citations_audit.py` added |
| `1ee68f76` | DB post migrations 010+011+track1 (user_version 9→11) |
| `325c25ce` | `sessions/LATEST` → 2026-05-13b |
| `2db970ce` | Fix broken architecture refs in PI v10.10 (`<surface>`→`<identity>`, `<bootstrap_exception>`→`<bootstrap_pattern>`, `<open_items>`→`<scope_assumptions>`) |
| `4cfe2946` | Architecture v2.3 amended: add caller-sweep pattern to `<migration_and_growth>` — direct lesson from the 4 broken refs that the first verification pass missed |

**Status:** captured in `session_2026-05-13b` close note ("repo reorganized (113 file ops across 6 batches); audit findings actioned") plus the caller-sweep lesson is recorded as the rationale in commit message of `4cfe2946` itself. **No additional session record needed.**

### 2026-05-14 (2 commits)

| Commit | Subject |
|---|---|
| `de364a88` | Add `audits/data-integrity-verification-plan.md` (6-phase plan, sequenced top-down, anchored to multi-lens-website integrity chain, level enforcement assigned per item) |
| `aa901d0a` | Write `sessions/handoff-next-session.md` (87 lines) |

**Status:** the handoff document substantially preserves state. It is not in `<session_close>` form (no session record), but for forward-execution purposes it is functionally equivalent: lists Phase 1.1 as next action, enumerates Phase 1.2/1.3/1.4 state, names known cross-rule signal (`PMP-A02-001-S2` cites `REF-00335` which is AUTHOR-TITLE-ONLY — bridge between rules #8 and #10). **No backfill session record will be authored; this session record points at the handoff as the canonical state-of-2026-05-14 artifact.**

### 2026-05-15 (44 commits, ~all morning + afternoon)

The substantive day. Three threads:

**Thread 1 — Skill authoring + PI v10.11 promotion (commits efde4328 → 80e2b426, 13:13–13:18 MDT):**
- `efde4328`: authored `skills/reasoning-doc-citations_SKILL.md` per PI rule #10 sub-rules 2/3 and DR-2026-05-13. Status `active`; enforcement Level 2 (audit at `scripts/audit/reasoning_doc_citations_audit.py`); companion to `adversarial-research` and `progressive-measurement`.
- `19d91608`: registered in `references/skill-registry.md` active table; removed from PI placeholders.
- `80e2b426`: PI v10.10 → v10.11. **Diff is 27 lines, surgical.** One skill line added to `<skills_assigned>`, one placeholder line removed, one changelog entry. No standing-rule changes, no XML-tag/section/path/identifier/schema/table renames or removals.

**Thread 2 — Audit-script and validator fixes (commits 69ebe9ab → 543760b8, scattered):**
- `69ebe9ab`: `citation_mining_completeness` rename SELECT cols to match `evidence_sources` schema (`author_display`, `pub_year`, `pub_title`).
- `1c40cfaa`: `validate_temporal` T-05 skip non-snapshot docs.
- `a2c5ff6d` + `8f2e06c3`: widen `DecisionStatus` enum to include `PROPOSED` and `PROVISIONAL`; update decision-capture audit counter.
- `0333f405`: restore truncated HIPI Lancet DOI in D01 KNOWN_DUP_DOIS list.
- `543760b8`: widen B04 valid set to accept DOI-resolver vocabulary; add `DIN 18040-1/-2` to D01 KNOWN list (CrossRef-confirmed intentional multi-section pattern).

**Thread 3 — DR-2026-05-15 (migration-history drift repair):**
- `4982f702`: DR-2026-05-15 proposed. Diagnoses that rebuilding from `scripts/migrations/*.sql` produces an `evidence_sources` table with 23 columns while the committed DB has 81. 8 tables exist in committed DB but no migration creates them. 11 entries in `data_migrations` document operations that were never committed as SQL files.
- `d5449e8f`: Option B baseline `012_baseline_2026-05-15.sql` applied — full schema+data dump as a new starting line. PASS on all 7 CI invariants + all 29 table row counts; FK clean.
- `5026e827`: `migrate_db.py` baseline-aware discovery — skip pre-baseline schema migrations and pre-baseline-timestamp data migrations during rebuild; honor baseline's own `PRAGMA user_version`.
- `9e8c2d1d` + `5070a223`: dedup migration `data_20260515200000` — 4 duplicate-DOI groups deduplicated (canonicals CrossRef-verified; 6 refs merged).
- `4d0e9b05` + `d36f55b3`: v1_legacy sync compensating for the dedup migration (C05/D02 invariants now match: 669=669, `ref_id` sets identical, FK clean).

**Status:** DR-2026-05-15 documents the thread. `migrate_db.py` change + baseline 012 represent a structural shift to a baseline-aware migration model (analogous to a database schema reset / squash in conventional migrations). Owner clearly chose and applied Option B based on commit history, but DR-2026-05-15 file still reads `Status: PROPOSED — awaiting owner directive`. **Anomaly to flag below; not changing the DR in this session without owner sign-off on whether Option B counts as adopted.**

---

## Anomalies (full list)

| # | Anomaly | Disposition this session |
|---|---|---|
| 1 | Bootstrap `Skills: $(grep -c '^### ' /tmp/registry.md) registered` returns 0; registry shape doesn't have `### ` headings | **Fix:** PI v10.12 drafted with corrected count helper. Queued in `PI-update-needed.md`. |
| 2 | `sessions/LATEST` stale: points at 2026-05-13b through ~51 commits of activity | **Fix:** bumped to this session record at session close. |
| 3 | `decisions/PI-update-needed.md` stale: reads "v10.10 deployment" while v10.11 is in fact live (this very chat loads v10.11 per session prompt) | **Fix:** replaced with current state (v10.11 live, v10.12 pending). |
| 4 | DR-2026-05-15 `Status: PROPOSED — awaiting owner directive` while commit history shows Option B was selected and fully applied (baseline 012, migrate_db.py change, dedup + sync migrations) | **Flag only:** noted here; owner to update DR header to `ADOPTED — Option B` if that reflects intent. Avoiding the edit without owner confirmation. |
| 5 | 2026-05-15 work absent from `sessions/` directory; only DR + commit messages preserved the trail | **Fix:** this session record captures the 51-commit reconciliation including the 2026-05-15 work-by-thread. |

## v10.10 → v10.11 caller-sweep determination

Per architecture v2.3 `<migration_and_growth>` "Removing or renaming structural elements," a caller-sweep is required when XML tag, section heading, file path, identifier, schema column, skill name, or table name is removed or renamed. Diff inspection:

- Header version line: v10.10 → v10.11 (expected).
- Changelog: one entry added.
- `<skills_assigned>`: `reasoning-doc-citations` line added to active block; same identifier removed from placeholder block. **Skill name was not renamed or removed — it was promoted from placeholder to active.** No callers cite the placeholder section in a way that breaks on this move (placeholders are an informational listing, not a referenced anchor).

**Result: no sweep required.** Recorded for the audit trail.

## reasoning-doc-citations skill provenance

| Field | Value |
|---|---|
| File | `skills/reasoning-doc-citations_SKILL.md` |
| Authored | commit `efde4328`, 2026-05-15 13:13 MDT |
| Registered active | commit `19d91608`, 2026-05-15 13:14 MDT |
| Promoted in PI | commit `80e2b426` (v10.11), 2026-05-15 13:18 MDT |
| Adopted-by | DR-2026-05-13 (`decisions/DR-2026-05-13-evidence-verification-methodology.md`) |
| Enforcement | Level 2 (audit at `scripts/audit/reasoning_doc_citations_audit.py`, committed `0297db5a` on 2026-05-13) |
| Governs | Citations in `references/bpc-reasoning/<slug>.md` supporting (a) jurisdiction-comparison cells (rule #9 step 3), (b) qualitative claims, (c) definitional claims |
| Companion skills | `adversarial-research`, `progressive-measurement` |

Provenance chain is complete and reconstructible from repo state.

---

## Actions taken this session

1. Authored this session record.
2. Drafted PI v10.12 at `governance/project-instructions-v10_12.md`. Patch is minimal: replaces the broken `grep -c '^### '` skill-count line with a backend-aware helper that counts `*_SKILL.md` files in the `skills/` GitHub directory (excluding `skills/deprecated/`). Changelog entry added.
3. Replaced `decisions/PI-update-needed.md` to reflect (a) v10.11 live, (b) v10.12 pending deployment.
4. Bumped `sessions/LATEST` to point at this session record.
5. Spot-check verification: confirmed architecture v2.3 caller-sweep section present at line 129 (commit `4cfe2946`); confirmed v10.10→v10.11 PI diff is 27 lines; confirmed `reasoning-doc-citations_SKILL.md` frontmatter links to DR-2026-05-13.

**Not done this session (explicitly out of scope):**
- DR-2026-05-15 status update (owner action — anomaly #4)
- Track 1 second pass (deferred per session_2026-05-13b handoff — content work, gated nothing here)
- Phase E.1 pilot BPC selection (next session, per session_2026-05-13b handoff — now unblocked by clean audit trail)

## Verification

- `ls sessions/session_2026-05-15a-governance-reconciliation.md` — present
- `ls governance/project-instructions-v10_12.md` — present
- `wc -l governance/project-instructions-v10_12.md` vs `v10_11.md` — line delta within ±5 (minimal patch)
- `cat sessions/LATEST` — reads `session_2026-05-15a-governance-reconciliation.md`
- `grep "v10.12" decisions/PI-update-needed.md` — present
- `git status --short` — only the four intended files; nothing else modified

(Verification block actually run is logged in commit messages on push.)

---

## Handoff

**session_close:** 2026-05-15 — governance trail reconciled 2026-05-13b → 2026-05-15; PI v10.12 drafted (bootstrap pattern fix); LATEST bumped; PI-update-needed refreshed.

**next_action:** (a) Owner: deploy PI v10.11 if not yet done; deploy v10.12 for the bootstrap fix; update DR-2026-05-15 header from PROPOSED to ADOPTED-OPTION-B if Option B was the directive (anomaly #4). (b) Next Claude session: Phase E.1 single-BPC pilot under `reasoning_doc_citations` workflow — pilot BPC selection is the first sub-task, then dry-run of the rule-#10 verification gate end-to-end on that BPC; load `audits/bpc-rewrite-workplan-2026-05-11.md` §Phase E for entry conditions.

**blockers:** Pilot BPC for Track 3 still not selected (carried from session_2026-05-13b). Choice criterion suggested: pick a BPC whose Phase B evidence pool already meets `metadata_quality = COMPLETE` AND `verification_status ∈ {VERIFIED, UNVERIFIED-1}` for ≥ 5 sources, to minimize "no eligible evidence" stalls during the pilot. SQL query for that filter is straightforward against `evidence_sources` + `source_slug_links`.

**Cross-rule signal carried forward:** `PMP-A02-001-S2` cites `REF-00335` which is `AUTHOR-TITLE-ONLY` → ineligible per rule #10 → invalidates the PMP walk per rule #8. First documented case of the cross-rule-8-and-10 bridge. Resolution path: either upgrade `REF-00335` metadata to COMPLETE (Track 1 work) or re-walk PMP with a different cited source. Not addressed this session.

**Audit trail integrity:** restored as of this commit. Next session can bootstrap on clean ground.

---

## Addendum — CI status at session close

Pushed commits land green on `Repo Integrity Audits` (source_slug_links duplicates, citation-mining completeness, migration reproducibility per `audit.yml`) and on the relevant `Guidebook CI` jobs (commit-msg format, syntax, schema, DB integrity). However, `Guidebook CI` overall remains **red** on this commit and has been red on every push since at least commit `0333f405` (2026-05-15 16:10) — ≥10 consecutive failing runs. Two pre-existing failures:

**Anomaly 6 — Structure validation: MISSING_SEARCH_LOG on ~30 BPC files.** `references/bpc/ALL-ENV.md`, `references/bpc/ALL-FW.md`, `references/bpc/_template.md`, and many domain BPC files have no matching search-log. Pre-existing drift unrelated to this session's work (BPC files untouched). Likely fallout from the bpc-rewrite-workplan-2026-05-11 restructuring; the search-log expectation is from the pre-rewrite era and may be obsolete OR the search logs were archived without updating the validator.

**Anomaly 7 — Governance validation: decisions.137 enum violation.** `decisions.137` has `effort_level: 200` and `model_routing: 'opus/200/synth'`, both outside current enum constraints (`{50|75|100|125|150}` for effort; `opus|sonnet|haiku|human|legacy / 150|125|100|75|50|none / synth|arbitrate|extract|format|route|none` for routing). Likely in-flight from the 2026-05-15 enum-widening commits (`a2c5ff6d` + `8f2e06c3`) that added `PROPOSED`/`PROVISIONAL` to `DecisionStatus` but did not also widen `effort_level` / `model_routing` enums to cover values now present in the register.

Both are pre-existing on commit `d36f55b3` (immediate predecessor of this session) and confirmed unrelated to this session's file changes (governance v10.12 patch + PI-update-needed + session record + LATEST). The team has been operating with red Guidebook CI for ~10 commits — implied force-merge posture.

**Next-session recommendation:** before the Phase E.1 pilot, decide whether to (a) fix the two CI failures and return Guidebook CI to green so the pilot lands on a clean baseline, or (b) accept the red CI as scope-out and proceed. Option (a) is preferred per the integrity argument that prompted this whole session; the `data-integrity-verification-plan.md` (2026-05-14) Phase 1.1 already calls for verifying CI passes, so addressing these is on-plan. The two fixes look small: extend `effort_level` and `model_routing` enums in `schemas/enums.py` (mirror the `DecisionStatus` widening pattern); for the BPC search-log expectation, decide if it's still applicable post-rewrite-workplan and either restore the search logs or update/disable that validator check.

---

## Second-half addendum — anomalies 4, 6, 7 worked in same session

Owner directive `proceed` (received after the initial addendum was pushed) authorized continuing on the queue. The session was extended.

### Anomaly #7 — Governance CI (resolved)

The validators live in `schemas/decision.py`, not `schemas/enums.py` as the first addendum guessed.

Root cause: D-0138 (Operative storage form selection, 2026-05-02) was authored at effort 200 with `model_routing: opus/200/synth` to signal a higher synthesis load than any prior session — but the schema constraints + `governance/decision-protocol.md` only enumerated `{150, 125, 100, 75, 50}`. The decision pre-dated the protocol's ability to express it. A second issue: D-0138 also used `review_status: PENDING` to express "awaiting project-owner adoption" — but the C8 rule says DG-NON requires `review_status=NA`. The "awaiting adoption" semantic was a status concept, not a review-status concept, and is now properly expressed by `status: PROVISIONAL` (which D-0138 already had; PROVISIONAL was added to the enum on 2026-05-15 in the same commit family).

Fix:
- `schemas/decision.py`: extended `MODEL_ROUTING_PATTERN` to permit `200`; extended `VALID_EFFORT_LEVELS` to include `200`; error message updated.
- `governance/decision-protocol.md`: amended §3.2 row 110, §4.2 row 164, §4.4 regex (line 185) to add `200`. §4.4 regex was also missing `legacy` from its protocol text despite the implementation accepting it — fixed in the same edit (pre-existing protocol-vs-implementation drift). Added explanatory paragraphs to §4.4: "Effort level 200 — when to use" (sparingly; multiple-per-quarter signals re-calibration) and "Legacy tier" (reserved for initial-seeding pattern per §5.3).
- `data/decisions/decision_register.yaml`: D-0138 `review_status` migrated `PENDING` → `NA` per C8; added migration note to D-0138's `notes` field explaining the semantic shift (status field now carries the "awaiting adoption" signal).

Verification: `python3 scripts/decision_capture.py` exits 0 locally. Register reports 1 PROPOSED / 2 PROVISIONAL / 147 ACTIVE / 0 SUPERSEDED / 0 RETIRED. WARNINGs remain on 4 pre-existing rationale-norm cases (C3/C6) — unchanged and not blocking.

Commit: `0cc4b8f5`.

### Anomaly #4 — DR-2026-05-15 status (resolved by owner directive)

Owner's `proceed` directive interpreted as authorization to mark DR-2026-05-15 ADOPTED — Option B, since the commit history (`d5449e8f` + `5026e827` + `9e8c2d1d` + `5070a223` + `4d0e9b05` + `d36f55b3`) shows Option B was selected and applied in full.

Fix: `decisions/DR-2026-05-15-migration-history-drift-repair.md` header `Status: PROPOSED → ADOPTED — Option B (Baseline Reset). Applied 2026-05-15 by owner via [commit list]. Header updated 2026-05-15 in session_2026-05-15a-governance-reconciliation.md upon owner directive.`

Commit: `af0b5abd`.

### Anomaly #6 — Structure CI (partial resolution; residuals flagged)

Root cause was a one-character path-name drift, not content drift: `scripts/validate_cross_refs.py` defined `SEARCH_LOG_ROOT = "references/search-logs"` (plural) while the actual directory in the repo is `references/search-log/` (singular). `scripts/validate_population.py` had the same orphan reference at line 305. Validator was glob-ing an empty directory and counted every BPC as `MISSING_SEARCH_LOG`. ~30 false-positive failures collapsed to:

- 4 real `MISSING_SEARCH_LOG` cases (BPCs without logs): `economics-sources`, `government-grant-programmes`, `ot-cpg-built-environment`, `school-environment-autism`
- 5 real `ORPHAN_SEARCH_LOG` cases (logs without BPCs, all economics-related): `economics-audit-cost-premium-cross-jurisdiction`, `economics-citation-chain-chandola-carnemolla`, `economics-japanese-housing-adaptation-costs`, `economics-research-session2-citation-mining`, `economics-session2-final-citation-mining`

Also added: skip underscore-prefixed BPC files (`_template.md`) in `collect_bpc_slugs` — templates aren't BPCs and shouldn't trip the co-existence check.

**Structure validation will still fail in CI** on the 9 residuals + a previously-masked set of `BROKEN_CON_ID` errors in `parts/v10/part04.md` and a few other files (the validator was bailing on the false-positive search-log block before reaching the CON-ID checks; lifting that block exposed the next layer). The 9 search-log residuals and the BROKEN_CON_ID set are real drift requiring owner judgment, not validator-typo cleanup — explicitly flagged for next-session triage rather than addressed here.

Commit: `632bddb5`.

### Out-of-scope finding flagged for next-session attention

`parts/v10/part04.md` and `parts/v10/part03.md` cite CON-0247, CON-0259..CON-0274 etc. which the validator reports as not present in the SQLite `connections` table. The mismatches were previously masked by the search-log validator bailing early. With the validator's false-positive search-log block cleared, these CON-ID references are now visible. Two possible repairs (not chosen this session):
1. Connections were renumbered in the database without updating `parts/v10/*.md` — fix the references in the markdown files.
2. Connections were dropped from the database without removing the references — restore the connections or remove the references.

Net CI improvement after the second-half work:
- Repo Integrity Audits: was green, still green.
- Guidebook CI Governance validation: red → **green** (was anomaly #7).
- Guidebook CI Structure validation: red → still red but now red on real issues (~9 search-log + ~17 BROKEN_CON_ID drift cases), not validator-typo false positives.

### Files touched in second half (5 commits total this session)

| Commit | Files |
|---|---|
| `c742d7f2` | `sessions/session_2026-05-15a-governance-reconciliation.md` (created), `sessions/LATEST` |
| `dd41dd0b` | `governance/project-instructions-v10_12.md` (created), `decisions/PI-update-needed.md` (replaced) |
| `30ecab78` | `sessions/session_2026-05-15a-governance-reconciliation.md` (first addendum) |
| `0cc4b8f5` | `schemas/decision.py`, `governance/decision-protocol.md`, `data/decisions/decision_register.yaml` |
| `af0b5abd` | `decisions/DR-2026-05-15-migration-history-drift-repair.md` |
| `632bddb5` | `scripts/validate_cross_refs.py`, `scripts/validate_population.py` |

(This appendix is itself a 7th commit on the same session record.)

### Revised handoff

**session_close (final):** 2026-05-15 — governance trail reconciled 2026-05-13b → 2026-05-15; PI v10.12 drafted (bootstrap pattern fix); LATEST bumped; PI-update-needed refreshed; anomaly #4 closed (DR-2026-05-15 ADOPTED — Option B); anomaly #6 substantially fixed (path-name drift cleared, residuals flagged); anomaly #7 closed (governance validation green).

**next_action (revised):** Phase E.1 single-BPC pilot under `reasoning-doc-citations` workflow. Pilot BPC selection criterion unchanged (≥ 5 sources at `metadata_quality = COMPLETE` AND `verification_status ∈ {VERIFIED, UNVERIFIED-1}`); a single SQL query against `evidence_sources` + `source_slug_links` will surface candidates. Before the pilot starts, owner may want a brief triage of the 9 search-log residuals and BROKEN_CON_ID set so Structure CI can return green — both look small.

**blockers (revised):**
- Pilot BPC for Track 3 still not selected (carried forward).
- Structure CI red on real residuals (9 search-log + ~17 BROKEN_CON_ID); not blocking pilot, but on the data-integrity-verification-plan.md Phase 1.1 acceptance criterion.

**Cross-rule signal carried forward (unchanged):** `PMP-A02-001-S2` cites `REF-00335` which is `AUTHOR-TITLE-ONLY` → ineligible per rule #10 → invalidates the PMP walk per rule #8. Resolution path: either upgrade `REF-00335` metadata to COMPLETE (Track 1 work) or re-walk PMP with a different cited source.

---

## Third-round addendum — BROKEN_CON_ID resolution + search-log residual triage

Owner directive `proceed` (third in the chat) authorized continued work on the Structure CI residuals flagged in the second-half addendum. Two threads: BROKEN_CON_ID set (resolved) and search-log residuals (triaged, policy-decisions surfaced).

### BROKEN_CON_ID set — resolved via data migration

**Root cause traced:** the missing CON-IDs were not validator drift — they were a real data loss. Historical thread reconstructed from git:

- **2026-05-06 14:05 (commit `3254705c`)**: synthesis-scan added CON-0253..CON-0274 (22 connections); combined with CON-0247..0252 added earlier in the same session-window, the connections table held 273 rows with max=CON-0274.
- **2026-05-07 21:43 (commit `412739f7`)**: "decision-capture: init tracking DB + migrations 001-005 + 86 items populated" — the DB was re-initialised and connections were reset to 0.
- **2026-05-13 20:38 (commit `d717bfae`)**: connections restored to 245 rows, max CON-0246. The restoration migration used a pre-2026-05-06 source; CON-0247..0274 were not in that source.
- **2026-05-15 baseline 012**: captured the 245-connection state as new starting line per DR-2026-05-15 Option B. Lost connections now absent from migration history entirely.

Twenty-eight markdown references to the lost CON-IDs remained in place (in `parts/v10/part03.md`, `parts/v10/part04.md`, `references/connections/_index.md`, `skills/citation-miner_SKILL.md`) — substantive content like CON-0264 "RT60 ≤0.4 s multi-population convergence" referenced as the universal acoustic target in `parts/v10/part04.md`. **This is the caller-sweep miss that architecture v2.3 `<migration_and_growth>` was authored to prevent** — the 2026-05-07 DB reset succeeded mechanically but left orphan markdown citations a sweep would have caught.

**Resolution:** authored `scripts/migrations/data_20260516030900_restore_synthesis_scan_connections_con_0247_to_0274.sql` (566 lines, 28 INSERTs + full header + `data_migrations` registration). Extracted source rows verbatim from the historical DB at SHA `3254705c`; same 13-column schema applies, no schema migration intervening. Sandbox applied cleanly (245 → 273 connections, max CON-0274, FK clean); committed-DB application followed. `validate_cross_refs.py` BROKEN_CON_ID count 17 → 0. Reproducibility: `migrate_db.py --rebuild /tmp/test.db` from baseline 012 + all data migrations including the new one produces 273 connections / max CON-0274 / 669 evidence_sources matching committed DB. (Note: rebuild's `data_migrations` table contains 3 more rows than committed — one per migration whose SQL also self-registers; this is a pre-existing pattern across the dedup migrations and not introduced here.)

Commits: `78dc9618` (migration file), `19c09b33` (DB application).

### Search-log residuals — policy decisions surfaced, not made

Nine real drift cases. Diagnosis shows two distinct sub-patterns; each requires owner judgment.

**4 BPCs without matching search-log:**

| BPC | Status | Disposition recommendation |
|---|---|---|
| `references/bpc/economics/economics-sources.md` | Index/meta-BPC | Likely warrants validator exemption — index BPCs aren't parameter BPCs and have no research pass to log. |
| `references/bpc/economics/government-grant-programmes.md` | Sibling of `government-grant-programmes-home-adaptation.md` which DOES have a matching log | Probably the parent/index of the home-adaptation BPC; same exemption category as above. |
| `references/bpc/population-general/ot-cpg-built-environment.md` | Real BPC, Co-2 OT clinical guidelines inventory, "Opus synthesis: YES" | Has substantive research content; the corresponding search-log was likely authored under a different filename or path during the 2026-03-28 work. Find it or re-author. |
| `references/bpc/sensory-environment/school-environment-autism.md` | Explicitly marked `STUB — new slug created B2. Full BPC research pass deferred.` | Search-log will be created when the BPC research pass runs (Phase E or later). Could add to a validator known-stub exemption list. |

**5 economics search-logs without matching BPC:**

| Search-log | Apparent type |
|---|---|
| `economics-audit-cost-premium-cross-jurisdiction.md` | Cross-jurisdiction research-audit log, not a parameter search-log |
| `economics-citation-chain-chandola-carnemolla.md` | Citation chain trace for two specific authors |
| `economics-japanese-housing-adaptation-costs.md` | Country-scoped sub-topic, not a parameter search-log |
| `economics-research-session2-citation-mining.md` | Session-2 citation-mining log (header explicitly says so) |
| `economics-session2-final-citation-mining.md` | Session-2 final citation-mining log |

All five appear to be **session-level research/citation-mining sub-logs**, not the 1:1-per-BPC search-logs the validator expects. The other 5 search-logs in `references/search-log/economics/` (`accessibility-feature-market-value-uplift-framing`, `accessible-design-economics-cost-premium`, `case-study-economics-financial-data`, `construction-cost-data`, `government-grant-programmes-home-adaptation`) DO match economics BPCs 1:1. So the 5 orphans are misfiled artifact-type — they likely belong in a `references/research-logs/` or `references/citation-mining-logs/` directory, or in `_archived/` as session artifacts.

**Recommended actions (owner judgment required, not taken this session):**
1. Decide whether index/meta-BPCs (`economics-sources`, `government-grant-programmes`) should be validator-exempt; if yes, either add an exemption list or a frontmatter flag (e.g., `bpc_type: index`).
2. Decide whether stub BPCs (`school-environment-autism`) get a known-pending exemption or are excluded from the 1:1 check until research runs.
3. Investigate the `ot-cpg-built-environment` search-log location — research was clearly done; the log file may exist under a different name.
4. Move the 5 economics session-citation-mining logs to an appropriate directory (`research-logs/` or `_archived/`) so the validator stops counting them as orphan search-logs.

These are all small mechanical operations once the policy direction is set. None are blockers for the Phase E.1 pilot.

### Final CI status

| Job | Status |
|---|---|
| Syntax check | ✓ |
| Commit message format | ✓ |
| Governance validation | ✓ (closed this session — anomaly #7) |
| Schema validation | ✓ |
| DB integrity | ✓ |
| Repo Integrity Audits (separate workflow) | ✓ |
| Structure validation | ✗ — 9 search-log residuals only; all BROKEN_CON_IDs cleared |

5 of 6 Guidebook CI jobs + Repo Integrity Audits = green. One remaining red job, on 9 cases requiring policy decisions surfaced above.

### Cumulative session ledger (9 commits)

| # | Commit | Concern |
|---|---|---|
| 1 | `c742d7f2` | session record + LATEST bump |
| 2 | `dd41dd0b` | PI v10.12 (bootstrap pattern fix) + PI-update-needed refresh |
| 3 | `30ecab78` | session record: first addendum (CI red baseline) |
| 4 | `0cc4b8f5` | anomaly #7 (governance CI) — enum widening + protocol + data record |
| 5 | `af0b5abd` | anomaly #4 — DR-2026-05-15 ADOPTED Option B |
| 6 | `632bddb5` | anomaly #6 (partial) — validator path fix + template skip |
| 7 | `0ebbad06` | session record: second addendum |
| 8 | `78dc9618` | data migration: restore CON-0247..0274 |
| 9 | `19c09b33` | apply migration to committed DB |
| 10 | (this commit) | session record: third addendum |
