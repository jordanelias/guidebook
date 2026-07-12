# Consolidation Remediation Roadmap

**Date:** 2026-07-12
**Prepared by:** Claude Code, at the owner's request, following `audits/consolidation-sweep-2026-07-12.md`.
**Status:** Proposal / reference — not itself a Decision Record. The two policy questions in this roadmap that require owner ratification are filed separately as `decisions/DR-2026-07-12-decision-tracking-naming-and-schema-doc-currency.md` and `decisions/DR-2026-07-12-versioning-and-archive-consolidation.md`.

This document does not restate `architecture/project-architecture-guidebook-v2.3.md`. That document already establishes the governing principles for most of what this roadmap addresses — a single canonical data layer, one archive convention, an enforcement spectrum for promoting text rules to code-checked rules. Where the sweep found a **gap in the existing architecture**, this document proposes new principles. Where it found **non-compliance with an already-stated rule**, this document proposes a remediation, not a new rule.

---

## What v2.3 already covers (compliance gaps, not architecture gaps)

- `<data_layer_pattern>`: "The SQLite database... is the single source of truth... Markdown files and JSON exports may derive from it but never compete with it." — governs the `data/guidebook.db` vs. `jurisdictional_values/*.yaml` split and any registry twin files once their provenance is confirmed (see sweep item flagged for owner verification).
- `<migration_and_growth>`: "Retiring content: move to `_archived/` rather than delete... subdirectories mirror the origin location." — governs the six parallel archive-ish locations found in the sweep. The rule exists; it isn't being followed everywhere.
- `<enforcement_spectrum>`: "If the rule is mechanically checkable AND drift is observably costly, promote to level 2 by writing an audit script." — this is the mechanism the new schema-reference-drift check (below) uses; it is not a new enforcement concept.

## New principles (genuine gaps in the existing architecture)

**1. Edit-in-place for governance documents; git history is the version log.**
v2.3 doesn't currently say anything about *how a governance document gets revised* — only how project data is versioned (migrations). The PI's 8-file version chain (`v10_7`–`v10_14`) and the armature 4-document design chain both show the same gap: nothing says "the current version lives at one stable path; prior text is `git log`, not a new file." Proposed rule: any document whose job is "state the current policy" (PI, architecture specs, tier system, mission) lives at one un-suffixed filename; revisions are commits, not new files. Documents whose job is "record a point-in-time decision or analysis" (DRs, audits, session logs) are correctly named with a date and should *not* be edited in place after the fact — the distinction is what the document is *for*, not a blanket rule.

**2. No dated snapshot files for registers; query git history instead.**
The gap register (3 dated snapshots) and tier-verification reports (5 dated snapshots, one pair a day apart) exist because "what did this register say on date X" was answered by copying the file instead of `git show`. Proposed rule: a register (gap register, connection register, decision register) has exactly one live path. If a point-in-time comparison is genuinely needed for a report, the report cites a commit SHA and/or embeds a git-diff excerpt, rather than committing a full copy of the register.

**3. Shared modules for logic implemented more than once.**
The DOI/CrossRef helper duplication (`crossref_doi_lookup`, `normalize_title_words` each defined twice) is a plain code-reuse gap, not a governance question. Proposed rule: `scripts/` gets a `scripts/lib/` (or similar) for logic used by more than one script; `resolve_dois.py` and `verify_resolved_dois.py` import from it instead of each defining their own copy.

**4. Disambiguate "Decisions" from "Decision Records."**
`data/decisions/decision_register.yaml` (D-NNNN) and `decisions/DR-YYYY-MM-DD-slug.md` are legitimately different things at different granularities, but nothing currently states that plainly in one place. Proposed rule: one sentence added to `architecture/project-architecture-guidebook-v2.3.md`'s `<reference_files_pattern>` naming the distinction, so a future session doesn't have to reverse-engineer it from context the way this sweep did.

**5. A canonical-vs-historical marker for architecture/schema documents.**
`schema-spec.md` and `schema-reconciliation.md` predate the current 192-migration schema and don't say whether they're still normative. Proposed rule: any `architecture/*.md` doc whose content can be superseded by the migrated schema itself gets a one-line status header — `Governs schema work: YES` or `Historical record only — see scripts/migrations/ for the current schema` — checked in the same pass as any future schema change.

**6. A named home and naming convention for handoff documents.**
Ten handoff files scattered across four directories. Proposed rule: `sessions/handoffs/handoff-<topic>-<date>.md`, matching the existing `sessions/LATEST` pointer convention; old locations get redirect stubs (see the pattern already proven at `references/connection-register.md`), not deletion.

**7. A parity check between paired-but-distinct twin trees.**
`bpc/` and `search-log/` are legitimately different content, but nothing verifies the pairing holds — a topic could gain a `bpc/` entry with no matching `search-log/` provenance record, or vice versa, and nothing would notice. Proposed rule: a level-2 audit script (see roadmap P1) checks filename-set parity between the two trees and reports orphans, without asserting anything about content.

---

## Prioritized roadmap

**P0 — data-correctness risk (already has draft DRs from the prior session; ratify or reject, don't leave open):**
- `evidence_cell_state` dual schema — `decisions/DR-2026-07-12-evidence-cell-state-schema-reconciliation.md`
- Tier-3 `stated` threshold — `decisions/DR-2026-07-12-tier3-stated-threshold.md`
- `data/guidebook.db` vs `jurisdictional_values/*.yaml` split
- **`scripts/generate/room_page.py` is currently broken** — references 6 tables absent from the live schema, found by the new drift-check script (see `audits/consolidation-sweep-2026-07-12.md` finding 8b). Unlike the other P0 items this one has no draft DR because it's a mechanical fix, not a judgment call: apply the same table-name correction already made in `spec_page.py`/`population_page.py`.

**P1 — active drift risk, moderate file counts, addressed by new principles above:**
- DOI/CrossRef helper duplication → shared module (Principle 3)
- PI 8-file version chain → edit-in-place (Principle 1)
- bpc/search-log parity check (Principle 7)
- Decision-tracking naming disambiguation (Principle 4)
- Schema-doc currency markers (Principle 5)

**P2 — low-risk cleanup, no active drift, cosmetic/historical:**
- Six archive locations → consolidate into `_archived/`, mirroring origin paths (per v2.3's already-stated rule)
- Gap-register and tier-verification snapshot pruning (Principle 2)
- Bibliography file consolidation
- Handoff-document relocation (Principle 6)
- Armature v3/v4 chain → a single consolidated "current armature" doc, with the four source documents moved to `_archived/`

## Executed this session

- This roadmap and the companion sweep audit.
- `decisions/DR-2026-07-12-decision-tracking-naming-and-schema-doc-currency.md` and `decisions/DR-2026-07-12-versioning-and-archive-consolidation.md` (both **PROPOSED**, pending owner ratification — Principles 1, 2, 4, 5, 6 above).
- `scripts/audit/schema_reference_drift_audit.py` — a level-2 audit script (additive, non-destructive; not wired into CI) that checks for table names referenced in `scripts/` source but absent from the live database, the specific failure mode behind the phantom-table bug already caught once in the website generators.

## Explicitly not executed this session

No existing file was merged, moved, or deleted: the archive locations, PI version files, armature files, bibliography files, gap-register snapshots, tier-verification reports, and handoff documents named above all stay exactly where they are until the owner reviews this roadmap. `scripts/migrations/` and `schemas/*.py` were not modified. `data/guidebook.db` and `data/jurisdictional_values/*.yaml` were not touched.
