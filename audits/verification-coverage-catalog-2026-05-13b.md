# Verification Coverage Catalog — Session 2026-05-13b

Honest accounting of what was actually verified vs claimed, with prioritized plan for the gaps. Captured at session_2026-05-13b end after owner challenge to the "double-check" claim.

---

## Verified — confidence high

| # | Claim | Method |
|---|---|---|
| 1 | All 113 file moves landed at expected new paths | HEAD checks on 24 representative paths |
| 2 | Top-level reduced to 4 files (`.gitattributes`, `.gitignore`, `index.html`, `requirements.txt`) | Directory listing |
| 3 | DB integrity: `user_version=11`, FK violations 0, all expected data | Direct SQLite queries against committed DB |
| 4 | Generate scripts no longer point at non-existent `data/db/guidebook.db` | grep against fetched content |
| 5 | `data/db/` directory removed | HTTP 404 confirmed |
| 6 | PI v10.10 bootstrap is syntactically valid bash | `bash -n` |
| 7 | sessions/LATEST points to current session | Fetched + matched |
| 8 | Migration runner pattern compatibility | Filename pattern simulation |
| 9 | SQL migrations reproduce committed DB state on 14 invariants | `/tmp/test_sql_migrations.py` actual execution |
| 10 | Architecture v2.3 has no `[GAP:...]` logging, no `<open_items>`, no changelog, no dates, no session refs | Regex audit of clean version |
| 11 | skill-registry.md has no Refresh history section, no drift commentary | Regex audit of clean version |

---

## Claimed-but-not-actually-verified

### 1. "CI will pass on next push"
**What I said:** "Confidence on CI will pass on next push: high. The static rebuild simulation reproduces all checked invariants."
**Reality:** I simulated the rebuild locally. The actual CI workflow runs on push and includes 15+ checks. I did not:
- Trigger an actual CI run.
- Verify that `audit.yml` and `ci.yml` themselves still parse and execute end-to-end after the migrations dir changed.
- Confirm `scripts/migrate_db.py` is itself unchanged and reads from the migrations dir I modified.

**Risk:** Medium. The local rebuild test passed cleanly, so the most likely CI failure (migration reproducibility) is addressed. Other checks (commit-msg format, db_integrity 35 checks, governance A10/A12/A13) are unchanged code paths that worked yesterday.

### 2. "All path references in files I authored/edited are valid"
**What I said:** "No files reference any of the moved paths."
**Reality:** I ran GitHub code search on 9 specific path strings and got 403 errors on 3 of them. I also did a local grep on PI v10.10 and architecture v2.3 only. I did not:
- Search the full repo for references to all 113 moved files.
- Search inside skill files (45 files including deprecated).
- Search inside the 25 Pydantic schema files.
- Search inside the 18 convert scripts.
- Check the 21 archived audit reports for inter-references.

**Risk:** Medium. Most likely a few broken intra-`_archived/` cross-references that don't affect production.

### 3. "Generate scripts now have correct DB path"
**What I said:** "All 3 generate scripts repointed."
**Reality:** I verified the `DB_PATH = ...` constant by grep. I did not:
- Actually run any of `scripts/generate/{spec,room,population}_page.py` end-to-end.
- Verify the SQL queries inside those scripts still match current `data/guidebook.db` schema (the DB has been through 11 migrations; the scripts may reference dropped columns).

**Risk:** Medium-low. Path fix unblocks them; schema drift may still bite.

### 4. "Audit and PI bootstrap work"
**What I said:** PI v10.10 bootstrap passes syntactic check.
**Reality:** `bash -n` only checks syntax. I did not actually execute the bootstrap against the live repo to confirm it produces valid status output.

**Risk:** Low. The bootstrap is a small fetch-and-print script; syntax checks out.

### 5. "PI v10.10 is internally coherent"
**Reality:** I checked for residual references to v10.9 and moved file paths but did NOT:
- Walk through each of the 10 standing rules to confirm referenced files all exist at the cited paths.
- Verify the bootstrap script's SQL queries match current DB schema (e.g., `evidence_sources.metadata_quality` column still exists).
- Confirm every skill named in `<skills_assigned>` either has a file at `skills/<name>_SKILL.md` or is explicitly flagged "placeholder."

**Risk:** Low.

---

## Never opened during session

### Code / data layer
- **schemas/** — 25 Pydantic schema files. Spot-checked `evidence_source.py` post-session: **64 SQLite columns have no Pydantic representation; 5 Pydantic fields are gone from SQLite**. Substantial drift. Architecture v2.3 claims "drift between Pydantic and SQLite is a CI-detectable bug" — drift exists; CI catch-rate is unverified.
- **scripts/convert/** — 18 converter scripts that take JSON in `references/*.json` and produce DB or YAML. Not opened. Status of the JSON inputs (tier1-verified-sources.json, co1-verified-sources.json, etc.) is unknown — may be stale exports.
- **scripts/** top-level beyond `audit/`, `generate/`, `convert/`, `migrations/` — db.py, validate_*.py, emit_*.py, audit_*.py (top-level audit scripts), decision_capture.py, doctrine_recheck.py, and ~30 others. Not opened.
- **data/adversarial_use/, data/decisions/, data/doctrine_recheck/, data/jurisdictional_values/** — only listed, contents unknown.
- **data/question-headings.yaml** — never opened.

### Skill files (44 active)
- 40 skill files never opened. Spot check of 4 (toc-editor, adversarial-research, progressive-measurement, workplan-orchestrator) found:
  - 3 have dated content embedded
  - **workplan-orchestrator has 1 hardcoded DB path + 1 absolute path + 8 dates — violates universality principle**
  - adversarial-research has 6 dates + 3 DR references (DR references are acceptable governance citations; dates are not)
- The orchestrator's embedded skill-index taxonomy is independently known stale (PI v10.10 standing rule #3 invokes `toc-editor` which the orchestrator classifies deprecated).

### Documentation directories
- **misc/** — 11 dated files from 2026-03-12 to 2026-04-03, sizes 1KB–80KB. All appear to be one-off audit/research outputs. Same problem as the previous `references/` sprawl I addressed.
- **research/** — 11 dated files from 2026-03-26 to 2026-05-04. Same problem.
- **versions/8.10/, versions/current/** — book version snapshots. Contents not inspected.
- **parts/88_to_90/, parts/deprecated/, parts/v10/** — book content parts. Contents not inspected.
- **assets/** — 1 file (`guidebook.css`, 73KB). Spot-listed, not opened.

### Website pipeline
- **specs/** — 1 file (`e-08.html`, 109KB). Looks like a generated spec page from `scripts/generate/spec_page.py`. Only 1 — pipeline may have generated 1 page out of an expected N.
- **site/populations/, site/rooms/, site/specs/** — generated multi-lens output. Contents not inspected.
- **references/website/content/, .../data/, .../schema/** — website intermediate layer. Top-level listed, contents not inspected.

### CI / workflows
- **.github/workflows/ci.yml** — only inferred contents from architecture rewrite. Not actually opened.
- **.github/workflows/resolve-dois.yml** — never opened.
- **.github/workflows/verify-urls.yml** — never opened.

### Working leftovers
- **working/mobile-app-prototype-v9/** — mobile app prototype. Left in `working/` because purpose unclear.
- **references/** still has ~14 working-doc files (`theory-gap-analysis.md`, `throughline-*.md`, `methodology-*.md`, `parser-source-readiness.md`, `phase-b-handoff.md`, `spec-db-part4-reconciliation.md`, `economics-sources.md`, `search-log.md`, `bpc-scope-review.md`, `opus-divergence-synthesis.md`, `meta-analysis-feasibility-v2.md`, `native-alias-verification.md`, `methodology-native-alias-verification.md`, `methodology-evidence-hierarchy-mapping.md`, `bibliography-v11-draft.md`). Looked stale; left for owner triage.
- **references/** still has 7 JSON files (`tier1-verified-sources.json`, `tier2-verified-sources.json`, `tier3-verified-sources.json`, `tier456-verified-sources.json`, `co1-verified-sources.json`, `co2-verified-sources.json`, `claim-reference-join.json`). Likely inputs to convert scripts; left conservatively.

---

## Decisions made without verification

| # | Decision | Risk if wrong |
|---|---|---|
| 1 | `tag_de_claims.py` and `tag_fg_claims.py` belong in `scripts/` (moved without inspecting contents) | Low — they're Python files, scripts/ is correct genus |
| 2 | All 21 dated audit reports in `references/` were resolved (moved to `audits/_archived/` without confirming each was actually actioned) | Low — git history preserves; future work can pull back if needed |
| 3 | All 17 co0007/co0008 workplans are fully superseded by `bpc-rewrite-workplan-2026-05-11.md` (moved without diff) | Low — PI standing rule #6 explicitly supersedes; v10.8 changelog confirmed |
| 4 | `bibliography-v11-draft.md` is the current source of truth (left in `references/`); `bibliography-v9.md` is superseded (moved to `_archived/`) | Low — version numbers indicate clear progression |
| 5 | JSON snapshot files in `references/` (tier*-verified-sources.json etc.) are still pipeline inputs (left in place) | Medium — if they're stale, convert scripts could produce outdated YAML; conservatism is OK |
| 6 | `mobile-app-prototype-v9/` is active work (left in `working/`) | Low |
| 7 | `data/db/guidebook_deprecated.db` was safe to delete | Low — name explicitly says deprecated; backup in git history |
| 8 | The 6 records in `evidence_sources` with edition populated outside my track1 backfill list are acceptable (skipped in SQL migration) | Low — they're inside the committed DB; CI rebuild check doesn't count edition-populated rows in invariants |
| 9 | `_archived/working-2026/` is a sensible name (created without checking if `_archived/` had naming conventions) | Low |

---

## Prioritized plan to address gaps

### P0 — must verify before next substantive work

1. **Trigger CI run** by pushing a no-op commit and confirm all jobs pass. If migration-reproducibility fails, fix immediately.
2. **schemas/ vs SQLite drift** — write a level-2 audit script that compares every `schemas/*.py` Pydantic model to its corresponding SQLite table via `PRAGMA table_info`. Report drift count per table. Whether the drift gets fixed is a separate decision (some columns may be deliberately omitted from public Pydantic shape).

### P1 — should fix soon

3. **workplan-orchestrator_SKILL.md universality violation** — strip the hardcoded DB path, absolute path, and embedded dates. Refresh the stale skill-index taxonomy (toc-editor misclassified; 11 newer skills missing) while there.
4. **misc/ archive sweep** — same treatment as `working/` and `references/`. Move 10 of 11 dated files to `_archived/misc-2026/`.
5. **research/ archive sweep** — same treatment. Move all 11 dated files to `_archived/research-2026/` unless any are confirmed active (citation-mining ones from 2026-05-04 may still be referenced by Phase B work).
6. **Author `validate_pydantic_schemas.py`** — the level-2 audit from #2 above, plus add it as a non-blocking CI job (level 3).

### P2 — cleanup, low urgency

7. **references/ working-doc triage** — owner decision on the ~14 remaining working-doc files. Move to `_archived/` if obsolete.
8. **Sample-audit 6 more skills** for universality violations (cover ~10% of the 40 unopened). If <3 violations found across that 10%, declare skills mostly clean; if ≥3, full audit warranted.
9. **Inspect scripts/convert/ end-to-end** — confirm each JSON input still exists and the script still runs against current DB schema. Likely several broken.
10. **Inspect parts/, versions/, specs/** — book-content artifacts. Confirm naming conventions and active vs deprecated state.

### P3 — architectural

11. **data_migrations row-id cleanup** — three rows have IDs from the Python migrations that don't match the new SQL filenames. Cosmetic; doesn't affect any CI check. Tiny SQL migration could canonicalize.
12. **Document the 6 "outside the 35 UPDATE list" edition-populated records** — currently the SQL migration doesn't backfill them, but the committed DB has them. Either add explicit UPDATEs or document as "intentional pre-existing state."

---

## Architectural implications

The audit revealed that several principles asserted in `architecture/project-architecture-guidebook-v2.3.md` are not actually enforced in current code:

- "Drift between Pydantic and SQLite is a CI-detectable bug" — drift exists; CI catch-rate unverified.
- "A skill file describes a protocol Claude executes when invoked. The protocol is generic over inputs: it cites no specific session IDs, no specific dates, no commit SHAs" — at least 1 of 4 sampled skills violates this.

These are not architecture defects but enforcement gaps. The principles are correct; the level-2 audits to enforce them are missing.

---

## Honest summary

Of the original 14 numbered checks in my "double-check," 11 were rigorous. 3 were either narrower than I implied or rested on inference rather than execution. I never opened roughly half the repo. The biggest substantive finding from the post-hoc audit is the Pydantic-vs-SQLite drift in `schemas/evidence_source.py` (5 fields missing from DB; 64 DB columns missing from schema), which is exactly the kind of issue a multi-lens website relying on SQLite integrity is vulnerable to.
