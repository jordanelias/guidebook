# Repo Strategy — CO-0007 Stage 0.8
**Created:** 2026-04-26 02:25 UTC
**Stage:** 0.8 (Repo strategy decision)
**Status:** Decision committed
**Decision authority:** Project owner (recorded 2026-04-26 in conversation)

---

## Decision

**Continue in `jordanelias/guidebook` `main`.** No new repo. No new branch.

Final repo decision deferred to **B1 (storage-form decision)** per workplan v3 §0.8 recommendation.

---

## Options considered (per workplan v3 §0.8)

| Option | Disposition | Reason |
|---|---|---|
| **Continue in `jordanelias/guidebook` main** | **CHOSEN** | See rationale below |
| Create `rebuild` branch in same repo | Deferred | Available later if B1 produces incompatible storage form |
| Create dedicated repo | Deferred | Premature — B1 has not selected storage form |
| Subdirectory in current repo | Rejected | No benefit over current top-level structure |

---

## Rationale

1. **B1 (storage form decision) is 26–40 sessions away.** Workplan v3 §0.8 explicitly recommends `rebuild` branch only as "defensible interim, with final decision deferrable to B1." Switching repos now is premature.

2. **The 2,259-commit history is part of the project's evidence trail.** First commit `e25429977715` (2026-03-18 05:25Z); HEAD at decision time `fd06b38b3eef` (2026-04-26). The corpus, doctrinal evolution, and Co-1 evidence were assembled in this repo. Orphaning it is a real cost; nothing else in workplan v3 requires it.

3. **All in-flight work lives here.** OPEN P1 gaps (GAP-079, GAP-CITE-01) reference paths in this repo. Stage-0 verification reports (committed `d1d7d450`, `0d569f74`, `3385209d`, `fd06b38b`) commit to `workplan/` in this repo. New repo would orphan or require migration.

4. **CI is configured for direct-push.** Project-standards rule 2026-04-19 02:20: branch protection DISABLED for Phase A direct-push workflow. Validators run on every push (post-hoc). New repo requires re-creating CI and the validators.

5. **B1 is when storage form is selected.** If B1 chooses graph DB, RDF, or relational, *that* is when the new infrastructure needs its own home — likely as a parallel repo or sibling branch with the markdown corpus migrated as input data. Until B1 chooses, the work is markdown-on-GitHub, which `main` already supports.

6. **No `rebuild` branch needed yet.** The branch makes sense once B1 forks architecture — a `rebuild` branch is one storage-form-decision option B1 might pick (if structured-markdown wins). Until then it's a directory of decisions and reports, fully home-able in `main`.

---

## Implications and operating rules during Stage 0 / Stage A / Stage B

- **Stage 0 outputs commit to `workplan/`** (already operating: `workplan/co0007-*.md`).
- **Governance documents commit to `governance/`** when produced. Directory created at first commit (this file is the first; created 2026-04-26).
- **Architecture documents commit to `architecture/`** when produced (Stage B1 onward). Directory created at first commit there.
- **Existing `references/`, `parts/`, `skills/`, `sessions/` continue as before.** No restructuring.
- **The 2026-04-19 02:20 rule (branch protection disabled) remains.** Direct-push workflow continues through Stage A.

---

## Trigger for revisit

This decision is revisited at **B1 (storage-form decision)**. At that point:

| If B1 chooses | Then |
|---|---|
| Structured markdown with build pipeline | Stay in same repo; no migration |
| Relational DB with views | Likely sibling repo or sub-directory (`db/`) for the database; markdown corpus stays as input to migration |
| Graph DB / triplestore / RDF | Likely separate repo for the graph backend; markdown corpus stays as input |
| Hybrid (relational + graph) | Decide per component |

The B1 decision document is the appropriate place to reopen this decision.

---

## Audit-trail entry

| Field | Value |
|---|---|
| Decision | Continue in `jordanelias/guidebook` `main` |
| Decided at | Stage 0.8 |
| Date | 2026-04-26 |
| Recorded in | This file |
| Revisit at | B1 (storage-form decision) |
| Decision authority | Project owner |
| Decision capture | This file is the audit-trail capture |
