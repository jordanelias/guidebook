# Data Integrity Verification Plan

Targets the multi-lens website's evidence chain: SQLite is the source of truth, derived artifacts must match, academic rigor requires both ends valid. Each item names what is checked, what level of enforcement applies, what the failure mode looks like for the website, and the smallest action that closes the gap.

Sequenced in dependency order. Earlier items establish ground truth; later items rely on it. Read top-down; execute top-down.

---

## Phase 1 — Confirm the data layer itself is sound

These checks ask: is `data/guidebook.db` what it claims to be? If any of these fail, everything downstream is compromised.

### 1.1 — Migration reproducibility check passes in actual CI

Push a no-op commit. Watch `.github/workflows/audit.yml` migration-reproducibility job. Confirm it completes with exit 0.

**Failure mode for website:** the committed DB cannot be regenerated from history → no defensible audit trail for any claim that cites the DB.

**Action:** push, observe, fix if failing. Local simulation already passed; this is empirical confirmation.

### 1.2 — Foreign-key integrity is zero violations on `main`

Add or confirm a CI check that runs `PRAGMA foreign_key_check` on `data/guidebook.db` and fails the job on any non-empty result.

**Failure mode for website:** orphan rows in derived tables produce phantom evidence — an item page citing a `ref_id` that no longer resolves to a source.

**Action:** check existing `audit.yml`; if the FK check isn't there as blocking, write a 4-line audit script and add the job. Level 4.

### 1.3 — Pydantic schemas mirror SQLite tables

Write `scripts/audit/validate_pydantic_schemas.py`. For each `schemas/*.py` Pydantic model, compare its declared fields to the corresponding SQLite table via `PRAGMA table_info`. Report (a) fields in Pydantic but not in DB, (b) columns in DB but not in Pydantic, (c) type mismatches. Document the acceptance criterion: which direction of drift is OK and why.

Known starting state: at least one model (`schemas/evidence_source.py`) has substantial drift in both directions.

**Failure mode for website:** front-end consumers of the API see one shape; the database stores another. Either columns are silently dropped from website queries, or website attempts to read columns that don't exist.

**Action:** write the audit; ship at level 2 first (manual CLI). Decide per-table whether each drift is intentional (some columns may be internal-only and deliberately omitted from Pydantic) or a bug to fix. Promote to level 4 once direction-of-drift policy is documented.

### 1.4 — Direct DB writes are detectable

The architecture asserts "direct writes that bypass migrations are prohibited; CI enforces reproducibility." Confirm this enforcement exists. The migration-reproducibility check (Phase 1.1) covers it in principle: a DB modified outside migrations will not rebuild identically. Verify by deliberate test in a branch: open an interactive shell, run an unrecorded `INSERT`, push to branch, observe the CI failure.

**Failure mode for website:** evidence enters the DB without an audit trail. Cannot defend the provenance of any specific cell.

**Action:** branch-based test. Document the outcome.

---

## Phase 2 — Confirm evidence quality at the row level

These checks ask: do the rows in `evidence_sources` and adjacent tables represent what they claim?

### 2.1 — Verification status is populated and means what it says

PI standing rule 10 names a verification gate: no synthesis claim may cite a source where `metadata_quality = AUTHOR-TITLE-ONLY` or `verification_status` is NULL.

The catalog notes the current state (at v10.8 adoption): 86% AUTHOR-TITLE-ONLY, 98% verification_status NULL. Track 1 (Pass 1) populated 41 records.

Confirm: (a) the gate is enforced — write the audit script that the v10.10 PI named but didn't yet ship, `scripts/audit/audit_evidence_metadata.py`; (b) the count of synthesis-eligible sources matches what was claimed at session close.

**Failure mode for website:** the website surfaces claims with citations that point at non-verified rows. The user sees authority that isn't there.

**Action:** ship the audit at level 2. Read counts. Add a row to the bootstrap status block with the synthesis-eligible source count so it appears every session.

### 2.2 — `evidence_population_match` rows are actually grounded

PI rule 7 requires `evidence_population_match` entries with `match_grade` per cited study. The expected pattern: every `ref_id` cited in `reasoning_doc_citations` or in a closed gap has at least one `evidence_population_match` row.

Write `scripts/audit/audit_evidence_population_match.py`. Report ref_ids cited in synthesis that have no population match recorded, and population-match rows whose `ref_id` no longer resolves.

**Failure mode for website:** an item page cites a study at face value when the study population doesn't match the target — e.g., a 65-and-over study cited on a school-age page.

**Action:** ship at level 2.

### 2.3 — PMP walks resolve to real values

PI rule 8 governs numerical specs. Every numerical-spec item should have `pmp_last_walk_at` populated; the walk's final row should cite a real `ref_id` whose metadata is COMPLETE.

`scripts/audit/pmp_audit.py` exists from this session. Run it. Confirm it produces the expected three findings (including PMP-A02-001-S2 citing REF-00335, which is AUTHOR-TITLE-ONLY). The findings themselves point at the rule 8 / rule 10 cross-rule signal.

**Failure mode for website:** a numerical spec page displays a measurement value that no peer-reviewed source actually validates.

**Action:** run pmp_audit; for each finding, decide remediation (re-walk, retract the spec, or upgrade the cited source).

### 2.4 — `reasoning_doc_citations` is populated as reasoning docs ship

DR-2026-05-13 Track 3 mandates per-cell verification recording. The audit script `scripts/audit/reasoning_doc_citations_audit.py` exists.

The audit reports rows where `value_match`/`claim_match` fields are not populated; reasoning-doc slugs cited but absent from the DB; and PAYWALL purchase candidates not yet decisioned.

**Failure mode for website:** synthesis output appears authoritative but its per-cell support has never been verified against the cited sources.

**Action:** the audit doesn't run on a meaningful corpus yet (Phase E.1 pilot hasn't started). Defer enforcement until the pilot ships rows. Then run weekly.

---

## Phase 3 — Confirm the website pipeline reads the DB faithfully

These checks ask: when SQLite says X, does the rendered page also say X?

### 3.1 — Generate scripts run end-to-end against current DB schema

The session fix repointed `scripts/generate/{spec,room,population}_page.py` at the correct DB path. Path fix alone doesn't guarantee the SQL queries inside still match a DB that has gone through 11 migrations.

Run each generate script. Capture: (a) does it complete without error; (b) does it produce output that diffs cleanly against the committed `specs/`, `site/specs/`, `site/rooms/`, `site/populations/` files?

**Failure mode for website:** the generation pipeline silently produces empty fields where a column it expects has been renamed or dropped. The website rolls forward with degraded content.

**Action:** execute each script. Document discrepancies. If any script breaks, decide per failure whether to update the script's query (preferred) or to repopulate the missing DB column.

### 3.2 — Generated pages match the DB content

Sample 5 spec pages, 5 room pages, 5 population pages. For each, pick three claims displayed and confirm each claim resolves to a specific row+column in the DB. The match must be exact: same value, same units, same citation.

**Failure mode for website:** the rendered page asserts something the DB does not support. This is the worst category — the website lies about its grounding.

**Action:** spot-check by hand. If discrepancy rate is non-zero, write a level-2 audit that walks the generation pipeline and re-checks every cell.

### 3.3 — Multi-lens consistency across surfaces

The same underlying data feeds the spec lens, room lens, and population lens. Pick 5 facts that should appear in at least two lenses. Confirm the value is identical across lenses.

**Failure mode for website:** the spec lens says 850mm; the room lens says 900mm; both cite the same source. The user has no way to know which is right.

**Action:** spot-check. If inconsistency found, the generation pipeline has duplicate copies of the source query rather than a single canonical join.

### 3.4 — Citation links resolve and point at real sources

For every `<cite>` (or equivalent) in generated pages: confirm the linked `ref_id` exists in `evidence_sources`, has `verification_status ∈ {VERIFIED, UNVERIFIED-1}`, and `metadata_quality = COMPLETE`. Any other state means the website is exposing a source that PI rule 10 says is ineligible for synthesis.

**Failure mode for website:** dead citation, retracted citation, or citation to a not-yet-verified source displayed as authoritative.

**Action:** walk the generated pages, extract all ref_ids, join against `evidence_sources`. Ship as `scripts/audit/audit_website_citations.py` at level 2; promote to CI once pipeline is stable.

---

## Phase 4 — Confirm the source rows themselves are real

These checks ask: when a row in `evidence_sources` claims to represent a paper, does that paper actually exist with the stated metadata?

### 4.1 — DOIs resolve

The repo has a `.github/workflows/resolve-dois.yml` workflow (not inspected in this session). Confirm it runs on schedule and the resolve rate is above an explicit threshold.

**Failure mode for website:** citations point at DOIs that 404. User clicks, sees nothing.

**Action:** open the workflow. Confirm scope (all VERIFIED rows?), schedule, and threshold. Document the current rate. Adjust threshold or scope if needed.

### 4.2 — Spot-check verification chain

Sample 10 sources with `verification_status = VERIFIED`. For each: open the cited URL or DOI. Confirm the title, authors, year, and edition match the DB row exactly.

This is the manual analogue of 4.1: verifies the metadata, not just the link.

**Failure mode for website:** the citation displays correct metadata, but the actual paper at the DOI is a different paper.

**Action:** spot-check by hand. If error rate is non-zero, the verification pipeline needs review.

### 4.3 — Track 1 second pass

The session's Track 1 first pass populated 41 records' `edition` field. ~600 catalog-fetch records remain. Continue Track 1 incrementally; each batch followed by a re-run of 2.1.

**Failure mode for website:** the website cites a 2010 standard but the cited claim derives from the 2018 edition's specific language. Edition mismatch invalidates the precision claim.

**Action:** schedule Track 1 batches across sessions. Update the row count in the bootstrap status block as it progresses.

---

## Phase 5 — Sustaining checks

These run continuously; they're how the integrity chain stays valid after Phases 1–4 close.

### 5.1 — Every PI standing rule has a corresponding audit at level 2 or above

Walk the 10 standing rules. For each, name the audit script that enforces it. Where the audit is missing, write it. The PI's `<hooks_status>` section enumerates current enforcement; close gaps until every numbered rule has at least level-2 coverage.

### 5.2 — Bootstrap status block reflects current integrity state

The bootstrap currently reports P1 OPEN, PMP backlog, AUTHOR-TITLE-ONLY count, NULL verification_status count, reasoning-doc coverage. Add: synthesis-eligible-source count (from 2.1), website-citation-validity rate (from 3.4), DOI-resolution rate (from 4.1).

The bootstrap becomes a per-session integrity dashboard. Any degradation surfaces immediately rather than at the next audit cycle.

### 5.3 — New skills and audit scripts are universal

Architecture `<skill_registry_pattern>` and `<enforcement_spectrum>` already require this. A caller-sweep audit (`scripts/audit/check_universality.py`) could check every active skill for: hardcoded paths, embedded dates, session_YYYY references, specific ref_ids, embedded changelogs. Level 2; runs weekly.

Catalog already documents one skill (`workplan-orchestrator_SKILL.md`) with three categories of violation. That skill is the first remediation target.

### 5.4 — Caller-sweep on every removal or rename

Architecture `<migration_and_growth>` documents the pattern. The lesson stays at level 1 (text) until evidence of repeat violation justifies a level-2 audit. Track violations across sessions. If recurrence ≥ 2, write `scripts/audit/check_orphan_refs.py` that takes a list of removed/renamed identifiers and reports orphan callers.

---

## Phase 6 — Continuous reconciliation

The deliverable is academic rigor. Academic rigor requires that the verification chain stay valid as the corpus grows.

### 6.1 — Each new synthesis batch passes Phases 2, 3, 4 in order

When the BPC rewrite workplan ships its next batch of reasoning documents, run 2.4 → 3.4 → 4.2 on the affected scope before merging.

### 6.2 — Audit findings move to gaps, not to backlogs

Audit script output that reports a real issue creates a row in `gaps` with priority and adversarial-research protocol fields. Backlogs that live in markdown files do not survive sessions; gaps in the DB do.

### 6.3 — Document the verification chain in user-facing form

The website itself should be able to display, for any rendered claim, the verification path: which DB row, which source, which verification status, which population match, which PMP walk if applicable. This is the deliverable the integrity chain exists to enable.

---

## Sequencing

| Phase | Blocking for | Typical session investment |
|---|---|---|
| 1 (data layer sound) | everything | 1–2 sessions |
| 2 (rows grounded) | 3, 4 | several sessions; Track 1 second pass is the largest item |
| 3 (pipeline faithful) | website publish | 1–2 sessions to write the audits; ongoing to run |
| 4 (sources real) | 6 | ongoing; Track 1 batches indefinitely |
| 5 (sustaining) | architectural quality | starts after 1 stable; continues forever |
| 6 (reconciliation) | publish-readiness | starts after 3 closes; per-batch |

Phase 1 is the precondition. If 1.1 fails on the next push, stop and fix before doing anything else.

---

## Acceptance criterion for "data integrity verified"

The integrity chain is verified when, for any claim a user sees on the website, the following can be reproduced in under five minutes:

1. The displayed value matches a specific row+column in `data/guidebook.db`.
2. The citation displayed alongside resolves to an `evidence_sources` row.
3. That row is `metadata_quality = COMPLETE` and `verification_status ∈ {VERIFIED, UNVERIFIED-1}`.
4. The cited source can be opened at its DOI or URL and the metadata matches.
5. The cited claim — exact value or qualitative statement — appears in the source at the cited location.
6. The population the source studied matches the target population displayed on the website (`match_grade ∈ {EXACT, PARTIAL}`).

When this chain holds for an arbitrary sample of 20 claims across all three lenses, academic rigor is defensible.
