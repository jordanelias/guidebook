# DR-2026-07-12: Decision-tracking naming disambiguation + schema-doc currency markers

- Status: **PROPOSED — pending owner ratification**
- Date: 2026-07-12
- Prepared by: Claude, following `audits/consolidation-sweep-2026-07-12.md`. Both changes below are additive documentation clarifications, not reinterpretations of existing rules — flagged as a DR anyway because they touch `architecture/project-architecture-guidebook-v2.3.md`, which is itself a ratified governing document.
- Affects (if ratified): `architecture/project-architecture-guidebook-v2.3.md` (`<reference_files_pattern>`), `architecture/schema-spec.md`, `architecture/schema-reconciliation.md`
- Related: `architecture/consolidation-remediation-roadmap-2026-07-12.md` (Principles 4 and 5), `audits/consolidation-sweep-2026-07-12.md`

## Context

The sweep found two unrelated small clarity gaps that share a common shape: a distinction is real and load-bearing, but nowhere written down, so a reader (or a future session) has to reverse-engineer it from context.

**Gap 1 — "Decisions" vs. "Decision Records."** `data/decisions/decision_register.yaml` tracks fine-grained decisions with IDs like `D-0001` (schema-validated per `governance/decision-protocol.md`, checked by `scripts/decision_capture.py`). `decisions/DR-YYYY-MM-DD-slug.md` (21 files) is the project's ADR-equivalent Decision Record series. Both are real, both are useful, and they are not duplicates of each other — but the naming ("Decisions" / "Decision Records") is close enough that nothing currently states the distinction in one place, and this sweep itself initially treated them as two representations of the same data before checking the ID schemes and validators.

**Gap 2 — schema-document currency.** `architecture/schema-spec.md` (Status: PROVISIONAL, dated 2026-05-02, "pending D-0138... adoption") and `architecture/schema-reconciliation.md` (Status: ACTIVE — "governs all downstream schema work", dated 2026-05-03) both predate the 192 files now in `scripts/migrations/`, which `architecture/project-architecture-guidebook-v2.3.md`'s `<data_layer_pattern>` already names as the authoritative schema source. Neither document states whether it remains normative guidance for schema changes today or is historical record of how the schema was originally designed.

## Proposed decision

1. Add one clause to `<reference_files_pattern>` in `architecture/project-architecture-guidebook-v2.3.md` stating: the `decision_register.yaml` (D-NNNN) tracks granular in-session decisions per the decision-capture protocol; `decisions/DR-*.md` (DR-dated) are standalone Decision Records analogous to ADRs. The two are related but distinct systems at different granularities, and neither supersedes the other.
2. Add a one-line status header to `architecture/schema-spec.md` and `architecture/schema-reconciliation.md` — `Governs schema work: NO — historical record; see scripts/migrations/ for the current schema` (or `YES` if the owner determines otherwise) — and add a note to `<migration_and_growth>` in `project-architecture-guidebook-v2.3.md` that any future `architecture/*.md` doc describing schema content carries this header from creation.

## Consequences if ratified

- No code or data changes. Both edits are additive clarifications to already-ratified governance text.
- Future architecture documents describing schema content are expected to declare currency status up front, reducing the odds of a repeat of the phantom-table pattern (a generator or doc treating stale schema description as current).
- No existing file is renamed, merged, or deleted by this DR.

## What would make this ACCEPTED

Owner confirmation that both statements above are factually correct (in particular, whether `schema-spec.md`/`schema-reconciliation.md` should actually be marked historical or are still meant to guide schema work — this DR assumes historical, since the live schema is the migrations, but that is the owner's call, not Claude's), followed by an explicit ratification note or session directive.
