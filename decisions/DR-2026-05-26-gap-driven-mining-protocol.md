# DR-2026-05-26 — Gap-Driven Mining Protocol

**Status:** **ACCEPTED — ratified by owner directive 2026-07-13 ("resolve all accept ratify all commit all"); see decisions/RATIFICATION-RECORD-2026-07-13.md** *(was: PROPOSED — pending owner adoption and worked-example pilot)*
**Authored:** 2026-05-26 (session_2026-05-26-gap-driven-mining-protocol-design)
**Doctrine SHA at authorship:** `61c7f95` (governance/mission-and-epistemics.md)
**Closes:** GAP-283 (citation-miner skill never invoked inline; structural pivot to gap-driven mining per owner direction 2026-05-23, session turn 14)
**Companion to:** `skills/citation-miner_SKILL.md` (anchor-source-keyed mining; this DR's protocol is gap-keyed)

---

## Context

The existing `citation-miner` skill is anchor-source-keyed. It starts from a confirmed Tier 1–3 source and traces backward + forward citations, depth-1 limit. This is a citation-graph operation: given an anchor, find its neighbors.

A second class of gap-closure work has no anchor to start from. Examples taken from the current OPEN gap set:

- `GAP-069` / `GAP-074` / `GAP-076` etc.: THIN-BASE flags on Vol II items where the evidence base is acknowledged as thin and a targeted literature review is the documented next step.
- `GAP-267` / `GAP-275`: "Co-1 evidence 0/24 jurisdictions" — the BPC's Co-1 anchor doesn't exist yet; mining has nowhere to start.
- `GAP-012` / `GAP-027` / `GAP-040`: "no indexed evidence for parameter X" — design criteria without source.
- `GAP-284`: "8+ standards named in session notes not promoted" — known sources awaiting verification + tiering, not awaiting discovery.

These gaps exist BECAUSE no anchor was found. Trying to close them by running `citation-miner` on the slug's existing anchor sources is the wrong shape — the anchors that exist are downstream of a different question than the gap is asking. The work has to start from the **parameter × population × outcome shortfall**, run an evidence search appropriate to the type of evidence being sought, and either find candidates that close the gap or log the null result.

This DR establishes the structural pieces that make that work auditable.

---

## Decision

### Input data structure — `gaps` with one new column

`gaps.mining_addressability` (TEXT, nullable, CHECK on enum) classifies each gap's resolution path:

| Value | Meaning |
|---|---|
| `ADDRESSABLE` | Gap-driven mining is the right resolution; protocol runs against this gap |
| `NOT-ADDRESSABLE` | Resolution path is something else (content authorship, structural fix, database correction); protocol does not touch this gap |
| `TRIAGE-NEEDED` | Classification deferred; pending review |
| `NULL` (pre-migration) | Treated as `TRIAGE-NEEDED` at query time |

A new `evidence_gaps` table was considered and rejected — the addressability concern is one column wide, and each `gap_id` maps 1:1 to a resolution path. A new table duplicates `gaps` content with sync risk.

### Triggers — both modes, batch primary

Mirrors `citation-miner`'s two-mode design:

- **BATCH (primary).** Sweep over `gaps WHERE status LIKE 'OPEN%' AND mining_addressability = 'ADDRESSABLE' AND priority IN ('P1','P2')`. One `gap_mining` row per attempt. Manual invocation per session; semiannual-sweep cadence inherits from DR-2026-05-24.
- **INLINE.** When another research skill is operating in a gap's neighborhood (e.g., `adversarial-research` closing a gap), it may call gap-driven-mining inline rather than waiting for next batch.

### Addressability classification — explicit triage with default class from `gaps.skill`

Each OPEN gap gets `mining_addressability` set explicitly by a one-time triage pass (a separate session, with the classification logged in a data migration with per-gap rationale). Default class is derived from `gaps.skill` to make triage tractable:

| `gaps.skill` value | Default | Override basis |
|---|---|---|
| `functional-deficit-auditor` | `ADDRESSABLE` | THIN-BASE flags are the canonical mining-addressable signal |
| `content-gap-analyzer` | `ADDRESSABLE` | "no indexed evidence" / missing-population coverage signals |
| `research-log-manager` | `ADDRESSABLE` | RP-category research shortfall signals |
| `bpc-auditor` | `NOT-ADDRESSABLE` | Audit findings about existing content; resolution is content edit |
| `guidebook-auditor` | `NOT-ADDRESSABLE` | Same |
| `citation-verifier` | `NOT-ADDRESSABLE` | Existing citation rejection; resolution is citation correction |
| `supersession-audit` | `NOT-ADDRESSABLE` | Supersession protocol (DR-2026-05-24) owns its resolution path |
| `citation-miner` / NULL / `-` | `TRIAGE-NEEDED` | Insufficient signal from skill alone |

Defaults are overridden at intake when the gap description signals a different shape — e.g., `GAP-283` is a `research-log-manager`-style architectural gap, not mining-addressable; its default `ADDRESSABLE` flips to `NOT-ADDRESSABLE` during triage.

Subsequent gap-raising skills (those that call `scripts/db.py add-gap`) set `mining_addressability` at creation. Backfill of legacy rows happens in the triage data migration.

### Output writes — new `gap_mining` table; reuse `evidence_sources` / `source_slug_links`

A new table `gap_mining`, modeled on `supersession_check` (DR-2026-05-24): one row per attempt, append-only. The most recent row per `gap_id` is the operative outcome.

The protocol writes:

1. `gap_mining` row per attempt, with `search_strategy_record`, `candidates_returned`, `candidates_reviewed`, `outcome`, `discoveries_logged`, `candidate_dois`, `check_method`, `notes`.
2. `evidence_sources` rows for verified discoveries — `discovery_method = 'gap_driven:GAP-NNN'`. Candidates returned but not yet verified are recorded as DOIs in `gap_mining.candidate_dois`, NOT INSERTed to `evidence_sources` (rule #10 gate; same pattern as `supersession_check.superseding_dois`).
3. `source_slug_links` rows linking discovered sources to the slug(s) the gap implicates.
4. `evidence_population_match` rows per discovery per rule #7's per-study population-match logging.

The protocol does NOT write `citation_mining` rows. That table's PK `(slug, local_ref_id)` is anchor-source-keyed; inserting gap-keyed rows would break the semantic.

### Per-gap stop condition — deterministic search matrix

Each gap pattern × target evidence type has a defined search matrix. Mining runs the matrix to completion (3 strategies; closure judgment happens after all return — composite cluster-search pattern per the supersession-audit lesson, ~5× fewer tool calls than per-query searches with no findings loss):

| Gap pattern | Primary | Secondary | Tertiary |
|---|---|---|---|
| THIN-BASE for primary clinical | PubMed RCT / OT-intervention (parameter+population) | Cochrane Library | Scholar Gateway |
| Co-1 0/N jurisdictions | Scholar Gateway lived-experience | Direct DPO catalogs | Multilingual-research handoff |
| No indexed evidence for numerical spec | PubMed (parameter+population, no tier filter) | Scholar Gateway → PMP follow-up | n/a |
| Cross-jurisdictional "standards not promoted" | Direct standards-body catalog | Multilingual-research | n/a |
| Cross-population invisibility | Population-coded PubMed query | Scholar Gateway | Multilingual-research |

The matrix is the protocol's spec for what counts as "looked." A gap that has not had every matrix entry attempted is not eligible for `null_result` — it's `deferred` at most.

### Cross-session idempotency — append-only, semiannual re-eligibility

`gap_mining` is append-only. Multiple attempts per gap are allowed; the operative outcome is the row with `MAX(attempt_at)`. A gap mined once with `null_result` is re-eligible after 6 months (mirrors the supersession-audit semiannual sweep). A gap with `partial_evidence_found` is re-eligible immediately if new candidate sources surface from any direction. A gap with `closure_evidence_found` does not re-trigger unless reopened.

This makes the protocol semiannual-sweep-ready: re-run the BATCH query filtered to `attempt_at < (today - 6 months)`, with publication-date filters set to `> previous attempt's attempt_at` to scope to truly new literature.

### Interlocks with existing rules

- **Rule #7 (adversarial research).** `outcome = 'closure_evidence_found'` requires populating `gaps.{falsification_condition, confidence_interval, shift_conditions, named_dissenter}` BEFORE the gap's `status` may transition to `CLOSED-*`. The protocol enforces this at the gap-status-transition step.
- **Rule #8 (PMP).** When the gap concerns a numerical specification value, the protocol's outcome cannot be `closure_evidence_found` until a `spec_value_probes` walk completes. The intermediate state is `partial_evidence_found` with `notes` recording the PMP queue.
- **Rule #10 sub-rules 2/3.** When discoveries land in a BPC reasoning document, `reasoning-doc-citations` runs on them per its existing protocol; the gap's closure is gated on those rows.
- **DR-2026-05-24 (supersession protocol).** When a gap-mining discovery supersedes an existing anchor in the slug's anchor set, a `supersession_check` row is created in addition to the `gap_mining` row. The two records describe orthogonal relationships: `gap_mining` answers "what closed this gap"; `supersession_check` answers "does the new evidence replace what an anchor was supporting."

---

## Out of scope (deferred to follow-up work)

- **The triage pass itself.** This DR defines what `mining_addressability` means and how the default class is derived. Running triage across the 36 currently-OPEN gaps is a separate session-scoped task (data migration with per-gap rationale).
- **The worked-example pilot.** Mirroring PI rule #10 Track 3, the first gap-driven mining run on a real `ADDRESSABLE` gap is a pilot with inline review before scaling. Pilot is post-adoption.
- **The skill file (`skills/gap-driven-mining_SKILL.md`).** The DR establishes the protocol; the skill file codifies how Claude executes it. Skill file is the immediate next-session deliverable.
- **PI rule update.** A new `<skills_assigned>` line for `gap-driven-mining` belongs in the next PI version bump. Architecture v2.3 `<migration_and_growth>` permits queuing this in `decisions/PI-update-needed.md` rather than shipping a PI bump for skill-assignment-only changes.
- **`scripts/db.py` CLI subcommands.** `add-gap-mining`, `update-gap` (for `mining_addressability`), and `unmined-gaps` query helpers ship with the skill file. The migration alone does not need them.
- **Automated sweep tooling.** Manual semiannual sweep suffices pre-launch, same posture as DR-2026-05-24.

---

## Decision rationale per mission test

1. **Helps readers ask better questions?** Yes — gap rows annotated with mining attempts surface which questions have been tested empirically and where the operative gap remains.
2. **Acknowledges non-uniformity?** Yes — the `partial_evidence_found` and `gap_recategorized` outcomes preserve heterogeneity rather than forcing each gap into binary close/open.
3. **Grounds best practice in evidence hierarchy?** Yes — search matrix is tier-prioritized per gap pattern; discoveries enter the evidence base only after rule #10 verification.
4. **Surfaces convergence/divergence?** Yes — discoveries from gap-driven mining feed into the same evidence base that supersession-audit and citation-miner operate on; cross-protocol divergence becomes auditable.
5. **Respects Co-1 operational reality?** Yes — Co-1 gap shape (e.g., "0/N jurisdictions") has its own search matrix entry routing to Scholar Gateway and direct DPO catalogs rather than PubMed.
6. **Teaches professional judgment?** Yes — every attempt's `search_strategy_record` is replayable; the audit trail shows what was looked for, where, and what was found or not found.
7. **Verifiable?** Yes — append-only `gap_mining` rows with full strategy records mean every claim that a gap is closed or open by mining is reconstructable from the DB.
8. **Aligns with audience priority?** Yes — designers and disabled-people audiences read claims grounded in current best evidence; the protocol prevents claims from drifting based on absent evidence going unaudited.

---

## Implementation deliverables

**This session (Pass 2a):**

1. **This DR** at `decisions/DR-2026-05-26-gap-driven-mining-protocol.md`.
2. **Migration 017** at `scripts/migrations/017_gap_driven_mining.sql` — adds `gaps.mining_addressability` column + `gap_mining` table. Schema 16 → 17.
3. **Attestation** at `attestations/decisions_DR-2026-05-26-gap-driven-mining-protocol.json`.

**Next session (Pass 2b):**

4. **Skill file** at `skills/gap-driven-mining_SKILL.md` — codifies the search matrix, BATCH and INLINE modes, rule #7/#8/#10 interlocks, depth-1 constraint inherited from `citation-miner`, attestation requirement.
5. **PI-update-needed entry** for the next PI bump (`<skills_assigned>` line addition).
6. **`scripts/db.py` CLI subcommands** for `gap_mining` writes and `mining_addressability` reads.
7. **Audit script** at `scripts/audit/gap_mining_audit.py` (Level 2): checks that every `OPEN` + `ADDRESSABLE` gap has at least one `gap_mining` row OR is annotated with a queued attempt; checks that `closure_evidence_found` outcomes have their rule #7 fields populated.

**Future session(s):**

8. **Triage data migration** — backfills `mining_addressability` for all OPEN gaps with per-gap rationale.
9. **Worked-example pilot** — first `ADDRESSABLE` gap mined end-to-end under the protocol; inline review before scaling.

---

## Status

PROPOSED 2026-05-26.

**Adopts upon:** migration 017 applied + skill file committed + worked-example pilot completed + at least one `gap_mining` row with each non-error outcome (`closure_evidence_found`, `partial_evidence_found`, `null_result`) demonstrated.

**Reversible by:** a follow-up DR that downgrades or replaces the protocol. The schema additions are forward-compatible — `gap_mining` rows are read-only audit history and `mining_addressability` is nullable.

---

## References

- `governance/mission-and-epistemics.md` doctrinal commitment 2 (best practice from evidence hierarchy, not code consensus)
- `governance/mission-and-epistemics.md` doctrinal commitment 3 (Co-1 co-primary with Tier 1)
- `governance/mission-and-epistemics.md` doctrinal commitment 5 (artifact traceability)
- `skills/citation-miner_SKILL.md` (anchor-source-keyed mining; this protocol's companion)
- `skills/supersession-audit_SKILL.md` (semiannual sweep cadence + cluster-search pattern this protocol inherits)
- `skills/adversarial-research_SKILL.md` (rule #7 — closure_evidence_found requires its 4-field output)
- `skills/progressive-measurement_SKILL.md` (rule #8 — numerical-spec gating)
- `skills/reasoning-doc-citations_SKILL.md` (rule #10 sub-rules 2/3 — reasoning-doc claim verification)
- `decisions/DR-2026-05-24-best-practice-supersession-protocol.md` (companion DR; same append-only-per-attempt design pattern)
- `decisions/DR-2026-05-13-evidence-verification-methodology.md` (rule #10 existence-and-content gate)
- `audits/bpc-rewrite-workplan-2026-05-11.md` §B.11 (citation mining; this DR is the gap-driven track owner pivoted to on 2026-05-23)
- Session record: `sessions/session_2026-05-23-bpc-rewrite-phase-b-closure.md` (P1 triage including GAP-283 annotation; "B.11 work on v1-eligible slugs is unblocked" — this DR provides the structural unblock)
