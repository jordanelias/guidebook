# Repo Strategy Revision — Change Order Proposal-of-Record
**Status:** PROPOSED — pending project-owner application
**Created:** 2026-05-02 02:50 UTC
**Predecessor document:** `governance/repo-strategy.md` (CO-0007 Stage 0.8, decided 2026-04-26)
**Trigger:** B1 storage-form selection per the predecessor's §"Trigger for revisit"
**Decision delegation:** D-OP / DG-REVIEW per A12 §2 (D-0140 PENDING)
**Doctrinal anchor:** D-0138 (storage form = SQLite, PROVISIONAL); `architecture/storage-derivation.md` §5

---

## 1. Purpose

The original `governance/repo-strategy.md` (Stage 0.8) decided to continue in `jordanelias/guidebook` `main` and explicitly deferred the **final** repo decision to B1 (storage-form decision). B1 Session 8 selected Candidate B (SQLite) as the operative storage form (D-0138 PROVISIONAL). This document is the proposal-of-record for the revision the original document anticipated.

The pattern follows `governance/pi-revision-co.md` (audit-remediation R6, D-0117): a Change Order proposal-of-record creates the audit trail; project-owner adoption applies the changes to the predecessor document.

## 2. Predecessor's anticipated outcomes vs actual

The predecessor's "Trigger for revisit" table predicted four outcomes per B1 storage-form selection:

| If B1 chooses | Predecessor predicted | B1 actually chose | Predecessor's prediction held? |
|---|---|---|---|
| Structured markdown with build pipeline | Stay in same repo; no migration | (rejected — Candidate A's adaptation pattern) | N/A (this branch not taken) |
| Relational DB with views | Likely sibling repo or sub-directory (`db/`) for the database; markdown corpus stays as input | Candidate B (SQLite) | **Partially.** The "sub-directory" prediction holds; the "sibling repo" alternative is rejected because SQLite's single-file form makes a sibling repo overhead without benefit. |
| Graph DB / triplestore / RDF | Likely separate repo for the graph backend | (rejected — Candidate C dismissed) | N/A |
| Hybrid | Decide per component | (rejected — Candidate D dismissed under D-0134) | N/A |

The predecessor's predictions were conservative pre-substrate-selection estimates. Now that SQLite is the operative substrate, the operative pattern is clearer.

## 3. Proposed revisions to `governance/repo-strategy.md`

### 3.1 Section "Decision" — update from deferred to terminal

Original text:
> **Continue in `jordanelias/guidebook` `main`.** No new repo. No new branch.
> Final repo decision deferred to **B1 (storage-form decision)** per workplan v3 §0.8 recommendation.

Proposed replacement:
> **Continue in `jordanelias/guidebook` `main`.** No new repo. No new branch. **Final repo decision: same repo, same main branch.**
> The deferred B1 trigger has resolved (per D-0138 PROVISIONAL → CANONICAL on adoption). Operative storage form is SQLite (single file at `data/db/guidebook.db`). Single-file substrate does not warrant repo separation.

### 3.2 Section "Implications and operating rules" — add operative artifacts

Add to the existing list:

> - **Architecture documents commit to `architecture/`.** Created at B1 Session 8. Current contents: `storage-derivation.md` (D-0138 PROVISIONAL), `schema-spec.md` (D-0139 PROVISIONAL).
> - **The operative SQLite database commits to `data/db/guidebook.db`.** Single binary file; treated as a generated artifact at B2 (rebuilt from canonical sources on each commit) OR as a versioned blob (committed directly with each change). B2 selects between these patterns.
> - **Migration tooling commits to `scripts/migrate/`.** Per `architecture/schema-spec.md` §5, 13-phase migration scripts live here.
> - **Validators commit to `scripts/`.** Existing pattern continues.
> - **The 2026-04-19 02:20 rule (branch protection disabled) remains.** Direct-push workflow continues through Stage B and into Stage C.

### 3.3 Section "Trigger for revisit" — supersede with terminal-state record

Original section reads:
> This decision is revisited at **B1 (storage-form decision)**. At that point:
> [4-row table with predictions]

Proposed replacement:
> ~~This decision is revisited at B1 (storage-form decision).~~ **B1 Session 8 (D-0138, 2026-05-02) selected SQLite as the operative storage form.** This decision's revisit-trigger has resolved.
>
> Future revisit triggers:
> - **A change in storage form** would re-trigger this decision. Per D-0138 §5.6, the SQLite selection is "revisable via formal D-METH amendment if the project's posture changes." Such an amendment would re-open this repo-strategy decision.
> - **A change in project posture** (e.g., team-scale operations replacing solo-author posture) might re-trigger evaluation of repo separation patterns (e.g., a separate repo for the corpus vs the tooling).

### 3.4 Section "Audit-trail entry" — append revision row

Append to the existing audit-trail table:

| Field | Value |
|---|---|
| Revision | Stage B1 — terminal-state revision |
| Revised at | B1 Session 9 (2026-05-02) |
| Revision authority | Project owner (via this Change Order adoption) |
| Decision capture | This Change Order document + D-0140 |
| Operative storage form | SQLite at `data/db/guidebook.db` per D-0138 |
| Repo decision | Same repo, same main branch (terminal) |

## 4. Adoption pattern

Project owner applies the revisions of §3 to `governance/repo-strategy.md` directly. On application, this Change Order document moves to `governance/applied-cos/repo-strategy-revision-co.md` (or the project's equivalent applied-CO archive directory) per the same pattern as `pi-revision-co.md` adoption.

If the project owner amends any of §3.1–§3.4 during adoption, the amendment is the operative text; this CO document records the proposed text but does not bind it.

## 5. Coordinations

- **D-0138 must be ADOPTED before this CO is applied.** D-0140 (this CO's record) explicitly predeces on D-0138; if D-0138 is amended in adoption (e.g., storage form changed), this CO is amended correspondingly.
- **migration-survival.md §7 forward-dependency on B1** triggers on D-0138 adoption; that document's CS-MIG cross-stage thread activates concurrently.
- **The `architecture/` directory is now operationally CANONICAL** (per B1 Sessions 8–9 deliverables) and should be added to the predecessor document's "operating rules" section per §3.2 above.

## 6. What this Change Order does NOT do

- Does NOT change the `main` branch decision.
- Does NOT add a `rebuild` branch (the predecessor's deferred option; not needed).
- Does NOT migrate the corpus to a separate repo.
- Does NOT amend project-standards or PI directly.
- Does NOT pre-decide B2's choice between "rebuild .db on each commit" vs "commit .db as versioned blob."

## 7. Status

| Field | Value |
|---|---|
| Document type | Change Order proposal-of-record |
| Status | PROPOSED — pending project-owner application |
| Decision record | D-0140 (D-OP / DG-REVIEW PENDING) |
| Predecessors | `governance/repo-strategy.md` (original); D-0138 (storage form selection); `architecture/storage-derivation.md`; `architecture/schema-spec.md` |
| Adoption pattern | Apply §3.1–§3.4 to predecessor; archive this CO to applied-COs |

## 8. Change log

- **2026-05-02 02:50** — Created at B1 Session 9 as Change Order proposal-of-record. PROPOSED.
