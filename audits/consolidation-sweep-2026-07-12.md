# Consolidation Sweep — Scattered Concepts and Fragmentation Catalogue

**Date:** 2026-07-12
**Prepared by:** Claude Code, three parallel recon passes (repo overview, git-history/recent-work sweep, dedicated duplication scan) followed by direct verification of the highest-stakes claims against actual file contents.
**Scope:** repository-wide, with emphasis on the last ~60 days of activity. This is a companion to, not a replacement for, `audits/project-inventory-and-state-2026-07-12.md`.

---

## Relationship to the prior audit

`audits/project-inventory-and-state-2026-07-12.md` (committed same day, PR #2) is a broad state-and-integrity audit. It already documents several fragmentation instances that this sweep reconfirms rather than rediscovers:

- `evidence_cell_state` defined incompatibly in `scripts/migrations/024_evidence_cell_state.sql` (item_code+population_code key) and `workplan/best-practices-assessment-system.md` §4 (slug+population+jurisdiction key), reconciled only in the still-**PROPOSED** `decisions/DR-2026-07-12-evidence-cell-state-schema-reconciliation.md`.
- The Tier-3 `stated`-threshold conflict between `governance/evidence-methodology.md` §2.2/§2.7 and `decisions/DR-2026-05-29-evidence-hierarchy-reconciliation.md`, addressed only in the still-**PROPOSED** `decisions/DR-2026-07-12-tier3-stated-threshold.md`.
- The `data/guidebook.db` vs. `data/jurisdictional_values/*.yaml` split — two parallel value stores, canonical `source_value_extractions` table empty while the YAML holds live data — flagged as "obscured" in the prior audit and still unresolved.
- Chronic `decisions/PI-update-needed.md` drift, open for months.

This document does not re-litigate those; it catalogues **additional** fragmentation this sweep found, verifies the highest-stakes claims directly against file contents (several initial hypotheses turned out to be wrong on inspection — noted below), and separates confirmed findings from ones that need an owner's semantic judgment before being treated as fact.

A note on method, because this project holds itself to an explicit evidence standard: three items below were initially suspected as duplication and are **not** — they are legitimate parallel-artifact patterns. Reporting them as fixed would have repeated the exact failure mode (`audits/_archived/`'s citation-fabrication incidents) this project has caught and re-caught before. They're included here specifically so the correction is on record.

---

## Confirmed findings (independently verified this session)

**1. `crossref_doi_lookup` and `normalize_title_words` are each defined independently in two files.**
`scripts/resolve_dois.py:590` and `scripts/verify_resolved_dois.py:61` both define `crossref_doi_lookup`. `scripts/resolve_dois.py:177` and `scripts/verify_urls.py:133` both define `normalize_title_words`. Verified by direct grep of function definitions. Risk: the two copies can silently drift (different retry/backoff logic, different normalization edge cases) with no test asserting parity.

**2. Eight Project Instructions files coexist as separate versions.**
`governance/project-instructions-v10_7.md` through `v10_14.md` — each revision is a whole new file rather than an edit to one file, so "what does the PI currently say" requires knowing which of 8 files is current. **Correction after adversarial review:** `architecture/project-architecture-guidebook-v2.3.md`'s `<migration_and_growth>` section explicitly *prescribes* this same new-file-per-revision pattern for PI specifically ("draft the corresponding PI bump in `governance/project-instructions-v<next>.md`"), for a stated reason — the PI is not API-writable and the owner must manually paste a full replacement into claude.ai project settings, so a stable single file wouldn't give them a complete document to copy. The 8-file accumulation is real, but the fix is not "stop versioning PI as new files" (that would contradict an already-ratified rule) — see the companion roadmap's revised Principle 1 for the corrected framing (archive superseded PI files promptly, don't leave them coexisting with the current one).

**3. Six archive-ish locations exist in parallel, outside the two conventions the project's own architecture doc names (`_archived/`, `workplan/_superseded/`).**
Verified file counts: `misc/archived/` (1 file), `_archived/misc-2026/` (10), `_archived/working-2026/` (10), `parts/_archived/` (22), `parts/deprecated/` (24), `parts/88_to_90/` (22) — 89 files total spread across locations a reader has to already know about to find retired content. `architecture/project-architecture-guidebook-v2.3.md`'s own `<migration_and_growth>` section already states the rule ("Retiring content: move to `_archived/` rather than delete... subdirectories mirror the origin location") — this is a compliance gap against an existing rule, not a missing rule.

**4. Two similarly-named but structurally distinct decision-tracking systems exist and could be confused with each other.**
`data/decisions/decision_register.yaml` tracks micro-decisions with IDs like `D-0001`, `D-0002` (validated by `scripts/decision_capture.py` per `governance/decision-protocol.md`). `decisions/DR-YYYY-MM-DD-slug.md` (22 files) tracks the project's ADR-equivalent Decision Records. These are **not duplicates of each other** — they're different granularities — but "Decisions" (D-NNNN) and "Decision Records" (DR-dated) are close enough in name that the distinction is not documented anywhere obvious, and a future session (human or model) could easily conflate them or file content in the wrong one.

**5. Schema described in three architecture documents whose currency relative to each other, and relative to the actual migrated schema, is not stated.**
`architecture/schema-spec.md` (Status: PROVISIONAL, pending D-0138 adoption, dated 2026-05-02) and `architecture/schema-reconciliation.md` (Status: ACTIVE — "governs all downstream schema work", dated 2026-05-03) both predate the 197 files now in `scripts/migrations/` (192 `.sql` migrations plus 5 stray non-SQL files — see finding 9 below), which is the actual authoritative schema per `architecture/project-architecture-guidebook-v2.3.md`'s `<data_layer_pattern>` ("The SQLite database... is the single source of truth"). Neither doc states whether it's historical record or still normative guidance for schema changes going forward.

**6. Tier-verification reports and gap-register snapshots are stored as one-off dated files rather than relying on git history for the "as of when" dimension.**
`audits/_archived/tier1-verification-progress-2026-04-23.md`, `tier2-...`, `tier3-...`, `tier456-...-04-23.md`, and a near-duplicate `tier456-...-04-24.md` one day later; `_archived/gap_register.md`, `gap_register_archive.md`, `gap_register_2026-03-20.md`. Git already records every historical state of a register at every commit (`git show <sha>:path`) — these snapshot files exist because that wasn't relied on.

**7. Ten "handoff" documents exist with no single canonical location or naming convention** (file existence verified via directory listing, not semantically reviewed):
`sessions/handoff-next-session.md`, `sessions/HANDOFF-2026-05-10.md`, `references/phase-b-handoff.md`, `workplan/co0009-phase0-handoff.md`, `workplan/a5-handoff.md`, `workplan/a6-handoff.md`, `references/audits/handoff-2026-05-12-verification-and-integrity.md`, `working/mobile-app-prototype-v9/HANDOFF.md`, plus 2 inside `sessions/session_2026-06-11-artifacts/`.

**8b. `scripts/generate/room_page.py` is currently broken against the live schema — the exact phantom-table bug already fixed elsewhere, missed in this file.**
Running the new `scripts/audit/schema_reference_drift_audit.py` (added by this sweep, see companion roadmap doc) surfaced this directly: `room_page.py` queries `FROM room`, `room_item`, `room_item_population`, `room_dar_provision`, `room_conflict`, and `specification` — none of which exist in the live `data/guidebook.db` (39 tables total via raw `sqlite_master` introspection, 38 excluding the internal `sqlite_sequence` bookkeeping table). `git log` shows the file hasn't been touched since 2026-05-28, predating the 2026-07-12 fix that rewrote the equivalent `spec_page.py` and `population_page.py` for the same phantom-table problem (per `audits/project-inventory-and-state-2026-07-12.md`) — `room_page.py` was evidently missed by that fix. All 6 flagged lines were independently confirmed to be live, reachable code (inside `query_room()`, called from `main()`), not comments or dead branches. **Correction after adversarial review — one nuance added:** `room_page.py` is not currently invoked by any CI workflow or other script, so this bug is dormant rather than actively corrupting anything today — the existing `site/rooms/*.html` pages are static output and unaffected. It would surface the moment someone next tries to regenerate room pages (`sqlite3.OperationalError: no such table`, confirmed by actually running the script), so it's still a real, worth-fixing bug — just not one silently producing wrong output on the live site right now.

**9. `scripts/migrate_evidence_sources_v2.py` references a table (`evidence_sources_v2`) that doesn't exist in the live schema — likely a stale, misplaced one-time migration script, not a live bug.**
Also surfaced by the drift-check script. Unlike `room_page.py`, this is a loose top-level file whose own docstring describes a one-time migration ("evidence_sources → evidence_sources_v2"), the same category as the historical scripts already excluded from the drift-check's live-surface scan when they sit in `scripts/db/`, `scripts/migrate/`, or `scripts/probes/` — this one simply isn't in any of those directories, so it wasn't excluded. Two things follow: (a) the drift-check's directory-based exclusion is porous — a script's "historical vs. live" status depends on which directory it happens to sit in, not what it actually does; (b) this specific file is itself a small instance of the fragmentation this sweep is about (a one-time migration script misplaced at the top level of `scripts/` instead of alongside its peers). Low priority — recommend relocating it during the P2 cleanup pass, not treating it as an active bug the way `room_page.py` is.

**10. Five session-specific scripts/data files sit inside `scripts/migrations/`, which per `architecture/project-architecture-guidebook-v2.3.md`'s `<data_layer_pattern>` should hold only numbered schema migrations and timestamped data migrations.**
`session_2026_05_11g_data.json`, `session_2026_05_11g_mine_ref00710.py`, `session_2026_05_11g_mine_ref00711_and_t3_verify.py`, `session_2026_05_11g_replay.py`, `session_2026_05_11g_t3_verify.py` — one-off session tooling, not forward-only SQL migrations, misfiled into the one directory this project's architecture doc treats as most strictly scoped. Low priority; recommend relocating to `sessions/session_2026-05-11g-*/` or an equivalent session-artifacts location during the P2 cleanup pass.

**8. Bibliography content has been rebuilt/re-snapshotted across 5+ files over time** (file existence verified, content overlap not individually diffed): `references/bibliography-v11-draft.md`, `_archived/references/bibliography-v9.md`, two `_archived/misc-2026/` compendium snapshots, two `bibliography-assembly-dryrun-*.md` files, plus two skill files claiming the same job (`skills/bibliography-compiler_SKILL.md` vs. deprecated `skills/deprecated/bibliography-updater_SKILL.md`).

---

## Corrected — initially suspected, verified NOT to be duplication

**A. `references/bpc/**` and `references/search-log/**` (97 matching relative paths) are NOT duplicated content.**
Direct comparison of a matched pair (`wayfinding-and-signage/luminance-contrast-lrv-evidence-base.md`) shows `bpc/` holds synthesized best-practice prose with citations and a consensus finding, while `search-log/` holds a structured YAML search-provenance log (per-language search status, query terms, source counts) for the *same* topic. This is a legitimate twin-track design (synthesis output + search provenance), not silent duplication. **Residual, lower-stakes finding:** no script verifies that every `bpc/` file has a matching `search-log/` entry and vice versa — a cheap parity check (not a merge) would catch orphans in either direction.

**B. `references/connection-register.md` is NOT a third file with unclear authority.**
It is an explicit, already-executed 9-line redirect stub ("This file has been split into... Do not add new entries to this file"), pointing to `connection-register-active.md` (pending entries) and `connection-register-archive.md` (resolved entries). This is a working example of exactly the kind of in-place consolidation this document recommends elsewhere (see Principle 2 in the companion architecture doc) — cited here as a positive precedent, not a problem.

**C. The four `armature_v3_review.md` / `v4.md` / `v4_integration.md` / `v4_resolutions.md` files are NOT version-proliferation like the PI files.**
Timestamps (2026-04-27 through 2026-04-28, same 2-day window) and headers ("Tri-Lens Review", "Pre-Decision... NOT decision-quality", "Judgment and Integration", "Open Question Resolution") show this is a single multi-stage design process (review → draft → integration → resolution), not one document forked repeatedly. The real gap is narrower than "duplication": **no single "here is the current, decision-quality armature" document exists** — a reader has to read all four and infer which parts are superseded by which.

---

## Adversarial verification pass

After the initial draft, three independent fresh-context reviewers (no memory of the reasoning above) were tasked with actively trying to refute this document's claims, the companion roadmap/DRs, and the drift-check script — rather than confirm them. Results: every substantive finding above held up (including 8b, reproduced end-to-end with an actual `sqlite3.OperationalError` traceback), but the review found and this revision corrects: a broken file-path citation (a bogus `governance/architecture/` prefix in finding 2, now fixed), four off-by-one file/table counts (findings 2/5/8b/A above), the missing dormancy caveat on 8b, and two real bugs in `schema_reference_drift_audit.py` itself (an f-string false-negative that was silently mislabeling three actually-referenced tables as unreferenced, and an unhandled crash on a malformed DB file) — both now fixed in the script, plus finding 9 (a table-reference miss the fixed script surfaced) and finding 10 (misplaced session scripts). One substantive flaw was found in the companion roadmap's reasoning, not this document — see `architecture/consolidation-remediation-roadmap-2026-07-12.md`'s revision note for what changed there.

---

## Flagged for owner verification (not independently confirmed this session — do not treat as fact)

- **`global-reference-registry.json` + `.md`, `claim-reference-join.json` + `.md`.** The `.md` registry carries a "Generated 2026-04-19" comment citing BPC tables as its source, and `scripts/convert/convert_sources.py` converts the `.json` into `EvidenceSource` schema records for migration — these may describe genuinely different pipelines (a citation-resolution registry vs. a one-time conversion input) rather than hand-maintained twins of the same data. Needs an owner read of both files, not an agent guess.
- **`references/specification-database.json` vs. `references/specification-database-schema.md`.** Not read this session; flagged only because both file names reference "specification database."

---

## Summary table

| # | Item | Status | Files (representative) |
|---|---|---|---|
| 1 | DOI/CrossRef helper duplication | Confirmed | `scripts/resolve_dois.py`, `scripts/verify_resolved_dois.py`, `scripts/verify_urls.py` |
| 2 | PI versioned as 8 files | Confirmed | `governance/project-instructions-v10_7.md`–`v10_14.md` |
| 3 | 6 parallel archive locations | Confirmed | `misc/archived/`, `_archived/misc-2026/`, `_archived/working-2026/`, `parts/_archived/`, `parts/deprecated/`, `parts/88_to_90/` |
| 4 | D-NNNN vs DR-YYYY-MM-DD naming collision risk | Confirmed | `data/decisions/decision_register.yaml`, `decisions/DR-*.md` |
| 5 | Schema described in stale/uncurrented docs | Confirmed | `architecture/schema-spec.md`, `architecture/schema-reconciliation.md` |
| 6 | Dated snapshot files instead of git history | Confirmed | `audits/_archived/tier*-verification-*.md`, `_archived/gap_register*.md` |
| 7 | Handoff docs, no canonical location | Confirmed (existence only) | 10 files across `sessions/`, `references/`, `workplan/`, `working/` |
| 8 | Bibliography rebuilt across 5+ files | Confirmed (existence only) | see above |
| 8b | `room_page.py` broken against live schema (found via new drift-check tool) | Confirmed, dormant bug | `scripts/generate/room_page.py` |
| 9 | `migrate_evidence_sources_v2.py` references dropped table | Confirmed, low priority | `scripts/migrate_evidence_sources_v2.py` |
| 10 | Session scripts misfiled in `scripts/migrations/` | Confirmed, low priority | `session_2026_05_11g_*` (5 files) |
| A | bpc/ vs search-log/ | Corrected — not duplication | — |
| B | connection-register.md | Corrected — already resolved | `references/connection-register.md` |
| C | armature v3/v4 files | Corrected — reframed | `governance/armature_v3_review.md` etc. |
| — | registry JSON/MD twins | Unverified — flagged only | `references/global-reference-registry.*` |

See `architecture/consolidation-remediation-roadmap-2026-07-12.md` for the principles and prioritized plan this catalogue feeds into.
